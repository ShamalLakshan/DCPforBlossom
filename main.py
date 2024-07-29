import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def get_vscode_extension_stats(extension_id="blossomtheme.blossomtheme"):
    url = f"https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;api-version=3.0-preview.1"
    }
    payload = {
        "filters": [
            {
                "criteria": [
                    {"filterType": 7, "value": extension_id}
                ]
            }
        ],
        "flags": 914
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['results'] and data['results'][0]['extensions']:
            extension = data['results'][0]['extensions'][0]
            statistics = extension.get('statistics', [])
            for stat in statistics:
                if stat.get('statisticName') == 'install':
                    return stat.get('value', 0)
        print("Extension not found or no download data available.")
        return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_sublime_package_stats(url, div_id):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with the specified ID
        target_div = soup.find('div', id=div_id)
        
        if target_div:
            # Return the text content of the div
            return target_div.text.strip().split(" ")
        else:
            return f"No div found with id '{div_id}'"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def main():
    # VS Code stats
    vscode_downloads = get_vscode_extension_stats()
    if vscode_downloads is not None:
        print(f"Number of downloads for your VSCode theme: {vscode_downloads}")

    # Sublime Package Stats
    sublime_downloads = get_sublime_package_stats(url = "https://packagecontrol.io/packages/Blossom%20Theme", div_id = "installs")
    if sublime_downloads is not None:
        print(f"Number of downloads for your Sublime theme: {sublime_downloads}")

if __name__ == "__main__":
    main()