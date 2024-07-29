import requests
from tabulate import tabulate

def get_reop_list():
    repo_url = "https://api.github.com/orgs/BlossomTheme/repos"
    repo_list = []

    response = requests.get(repo_url)
    
    if response.status_code == 200:
        repositories = response.json()
        for repo in repositories:
            repo_list.append(repo["name"])
    # After this add code to do fun and useful things with the repository information!
        return repo_list

    # If status_code is not 200, something is wrong with our request
    else:
        print(f"Failed to retrieve repositories. Status code: {response.status_code}")

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
    info = get_org_info()
    table = []
    for stat in info:
        row = [stat, info[stat]]
        table.append(row)

    print(tabulate(table, headers = ["Stat", "Info"], tablefmt="github"))

if __name__ == "__main__":
    main()
