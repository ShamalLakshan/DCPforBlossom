import requests

def get_obsidian_theme_installs(theme_id):
    url = "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-css-themes.json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        themes = response.json()
        for theme in themes:
            if theme.get('id') == theme_id:
                return theme.get('downloads', 0)
        print(f"Theme with ID '{theme_id}' not found.")
        return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

theme_id = "Blossom"

installs = get_obsidian_theme_installs(theme_id)
if installs is not None:
    print(f"Number of installs for your Obsidian theme: {installs}")