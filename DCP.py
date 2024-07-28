import requests
from bs4 import BeautifulSoup

def get_div_content(url, div_id):
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
            return target_div.text.strip()
        else:
            return f"No div found with id '{div_id}'"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

# Example usage
url = "https://packagecontrol.io/packages/Blossom%20Theme"
div_id = "installs"

content = get_div_content(url, div_id)
print(content)
