import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tabulate import tabulate
import os


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


def get_repo_list():
    repo_url = "https://api.github.com/orgs/BlossomTheme/repos"
    repo_list = []

    response = requests.get(repo_url)
    
    if response.status_code == 200:
        repositories = response.json()
        for repo in repositories:
            repo_list.append(repo["name"])
        return repo_list

    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")


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


def get_org_info():
    repo_url = "https://api.github.com/users/BlossomTheme"
    information = {}

    response = requests.get(repo_url)
    
    if response.status_code == 200:
        stats = response.json()
        for info in stats:
            information[info] = (stats[info])
        return information

    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")


def main():
    filename = ("./logs/" + (datetime.now().strftime("%d") + "-" + datetime.now().strftime("%m") + "-" + datetime.now().strftime("%Y")) + ".md")
    file = open(filename, "a") 

    file.write("# Blossom Theme Stats \n \n")

    # Organization Information
    print("## Organization Stats")
    file.write("## Organization Stats \n")
    info = get_org_info()
    table = []
    for stat in info:
        row = [stat, info[stat]]
        table.append(row)

    print(tabulate(table, headers = ["Stat", "Info"], tablefmt="github"))
    file.write(tabulate(table, headers = ["Stat", "Info"], tablefmt="github"))
    file.write("\n \n")

    # VS Code stats
    vscode_downloads = get_vscode_extension_stats()
    if vscode_downloads is not None:
        print()
        print("## VS Code Stats")
        file.write("## VS Code Stats \n")

        headers = ["Type", "Amount"]
        table = [["Total Downloads", vscode_downloads]]

        print(tabulate(table, headers, tablefmt="github"))
        file.write(tabulate(table, headers, tablefmt="github"))

    print()
    file.write("\n \n")

    # Sublime Package Stats
    sublime_downloads = get_sublime_package_stats(url = "https://packagecontrol.io/packages/Blossom%20Theme", div_id = "installs")
    if sublime_downloads is not None:
        print()
        print("## Sublime Stats")
        file.write("## Sublime Stats \n")
        headers = ["Type", "Amount"]
        table = [["Total Downloads", sublime_downloads[0]], ["Windows Downloads", sublime_downloads[1]], ["Mac Downloads", sublime_downloads[2]], ["Linux Downloads", sublime_downloads[3]]]
        print(tabulate(table, headers, tablefmt="github"))
        file.write(tabulate(table, headers, tablefmt="github"))

        print()
        file.write("\n \n")

        # Repository clones
        print()
        print("## Repository Clones")
        file.write("## Repository Clones \n")
        repo_list = get_repo_list()
        try:
            SOME_SECRET = os.environ["SOME_SECRET"]
        except KeyError:
            SOME_SECRET = "Token not available!"

        token = SOME_SECRET
        owner = "BlossomTheme"
        table = []

        for repo in repo_list:
            num_of_clones = get_clone_count(owner, repo, token)
            repo_and_clones = [repo, num_of_clones]
            table.append(repo_and_clones)
        
        print(tabulate(table, headers, tablefmt="github"))
        file.write(tabulate(table, headers, tablefmt="github"))

        
        file.close()
        

if __name__ == "__main__":
    main()