import requests

def get_vscode_extension_stats(extension_id):
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

# Replace with your VSCode theme's extension ID
extension_id = "blossomtheme.blossomtheme"

downloads = get_vscode_extension_stats(extension_id)
if downloads is not None:
    print(f"Number of downloads for your VSCode theme: {downloads}")