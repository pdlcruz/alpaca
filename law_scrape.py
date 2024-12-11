import requests
import os

SAVE_DIR = "./uscode_files"
os.makedirs(SAVE_DIR, exist_ok=True)
USCODE_URL = "https://api.govinfo.gov/collections/USCODE"

API_KEY = "cSYlWWbxe6j9iAfHW6cAQq0Wy4rxnyJJBd3gcQp9"
BASE_URL = "https://api.govinfo.gov/collections"

def fetch_collections():
    """Fetch list of available collections from the GovInfo API."""
    params = {
        "api_key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print("Collections available:")
        for collection in data.get("collections", []):
            print(f"- {collection['collectionCode']}: {collection['collectionName']}")
    except requests.RequestException as e:
        print(f"Error: {e}")



def fetch_uscode_metadata():
    """Fetch metadata for the USCODE collection."""
    params = {
        "api_key": API_KEY
    }
    try:
        response = requests.get(USCODE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print("U.S. Code Metadata:")
        for item in data.get("packages", []):
            print(f"Package ID: {item['packageId']} - {item['title']}")
        return data.get("packages", [])
    except requests.RequestException as e:
        print(f"Error fetching USCODE metadata: {e}")
        return []


def download_all_uscode():
    """Fetch and download all USCODE packages."""
    packages = fetch_uscode_metadata()
    for package in packages:
        package_id = package.get("packageId")
        if package_id:
            download_uscode_package(package_id)


fetch_collections()
fetch_uscode_metadata()
download_all_uscode()