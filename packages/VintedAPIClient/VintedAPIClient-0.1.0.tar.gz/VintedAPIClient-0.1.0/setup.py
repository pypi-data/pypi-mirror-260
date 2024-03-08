from setuptools import setup, find_packages

setup(
    name="VintedAPIClient",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    python_requires='>=3.6',
    description="Python client for scraping Vinted website",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/giaco8020/VintedScraper",
    author="Giaco8020",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
