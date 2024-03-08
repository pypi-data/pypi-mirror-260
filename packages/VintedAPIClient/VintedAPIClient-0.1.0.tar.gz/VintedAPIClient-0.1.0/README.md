
# VintedAPIClient

## Installation

You can install the package using pip:

```bash
pip install VintedAPIClient
```

## Usage


```python
from VintedAPIClient import VintedAPI

# Initialize the API client
api = VintedAPI()

# Retrieve a list of items based on a search query
# query: String containing the search keywords
# page: Integer indicating the page number to retrieve (approximately 100 items per page)
items = api.get_list_items("query", page)

# Download images for a specific item
# url: Vinted URL corresponding to an item
# destination_folder: Folder path where the images should be saved
# Images will be saved sequentially as "imgNUMBER.jpg"
api.download_images_by_url(url, destination_folder)

```

