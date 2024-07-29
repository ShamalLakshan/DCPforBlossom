import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tabulate import tabulate


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
            downloads = [target_div.text.strip().split(" ")[4], target_div.text.strip().split(" ")[8], target_div.text.strip().split(" ")[13], target_div.text.strip().split(" ")[18]]

            return downloads
        else:
            return f"No div found with id '{div_id}'"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def get_clone_count(owner, repo, token, days=14):
    # GitHub API endpoint for clone statistics
    url = f"https://api.github.com/repos/{owner}/{repo}/traffic/clones"
    
    # Headers for authentication
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter and sum clones within the date range
        total_clones = sum(
            item['count'] for item in data['clones']
            if start_date <= datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%SZ") <= end_date
        )
        
        return total_clones
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def main():
    # VS Code stats
    vscode_downloads = get_vscode_extension_stats()
    if vscode_downloads is not None:
        print()
        print("# VS Code Stats")
        headers = ["Type", "Amount"]
        table = [["Total", vscode_downloads]]
        print(tabulate(table, headers, tablefmt="github"))

    print()

    # Sublime Package Stats
    sublime_downloads = get_sublime_package_stats(url = "https://packagecontrol.io/packages/Blossom%20Theme", div_id = "installs")
    if sublime_downloads is not None:
        print()
        print("# Sublime Stats")
        headers = ["Type", "Amount"]
        table = [["Total", sublime_downloads[0]], ["Windows", sublime_downloads[1]], ["Mac", sublime_downloads[2]], ["Linux", sublime_downloads[3]]]
        print(tabulate(table, headers, tablefmt="github"))

        print()


        

if __name__ == "__main__":
    main()