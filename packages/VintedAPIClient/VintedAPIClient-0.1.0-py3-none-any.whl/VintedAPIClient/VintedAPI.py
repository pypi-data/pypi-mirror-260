import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote_plus, urlparse


class VintedAPI:
    def __init__(self, base_url="https://www.vinted.it"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "authority": "www.VintedAPIClient.it",
            "method": "GET",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Linux\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.session.headers.update(self.headers)
        self.last_token_refresh = None

    def _refresh_token_if_needed(self):
        if self.last_token_refresh is None or (datetime.now() - self.last_token_refresh).total_seconds() > 600:
            self._get_token()

    def _get_token(self):
        self.session.cookies.clear()
        response = self.session.get(self.base_url)
        if response.status_code == 200:
            self.last_token_refresh = datetime.now()
            return 0
        else:
            return -1

    def get_list_items(self, query, num):
        self._refresh_token_if_needed()
        encoded_query = quote_plus(query)
        url = f"{self.base_url}/api/v2/catalog/items?page={num}&per_page=96&search_text={encoded_query}&catalog_ids=&size_ids=&brand_ids=&status_ids=&color_ids=&material_ids="
        #print(url)

        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            items = [
                {
                    "id": item.get("id"),
                    "name": item.get("title"),
                    "item_url": f"{self.base_url}/items/{item.get('id')}"
                }
                for item in data.get('items', [])
            ]
            return {"success": True, "data": {"items": items}}
        else:
            return {"success": False, "statusCode": response.status_code, "message": "Failed to fetch data"}

    def download_images_by_url(self, url, destination_folder):
        self._refresh_token_if_needed()
        domain_parts = urlparse(url).netloc.split('.')
        if len(domain_parts) < 3 or domain_parts[0] != 'www' or domain_parts[1] != 'vinted':
            return {"success": False,
                    "message": "Domain must be 'www.vinted' "}

        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.select('section.item-photos__container img')
            last_file_number = self._get_last_file_number(destination_folder)

            for img in images:
                img_src = img.get('src')
                if img_src:
                    last_file_number += 1
                    file_name = f"img{str(last_file_number).zfill(2)}.jpg"
                    file_path = os.path.join(destination_folder, file_name)
                    img_data = self.session.get(img_src).content
                    with open(file_path, 'wb') as file:
                        file.write(img_data)

            return {"success": True, "data": len(images)}
        else:
            return {"success": False, "statusCode": response.status_code, "message": "Error downloading images"}

    def _get_last_file_number(self, destination_folder):
        existing_files = [f for f in os.listdir(destination_folder) if f.endswith('.jpg')]
        return int(existing_files[-1].replace('img', '').replace('.jpg', '')) if existing_files else 0


