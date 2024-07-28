import requests
from datetime import datetime, timedelta

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

owner = "BlossomTheme"
repo = "MusicBee"
token = ""

clone_count = get_clone_count(owner, repo, token)
if clone_count is not None:
    print(f"Number of clones in the last 14 days: {clone_count}")