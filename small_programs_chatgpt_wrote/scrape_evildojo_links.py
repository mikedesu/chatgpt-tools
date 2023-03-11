# generated on 12-26-2022

"""
Please write me some Python code. I need a small script that performs a get request to the website https://www.evildojo.com and then returns the every hyperlink on the page as a list of strings.
"""

import requests
from bs4 import BeautifulSoup

# Perform the GET request to the website
response = requests.get('https://www.evildojo.com')

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the hyperlinks in the page
    links = soup.find_all('a')

    # Extract the href attribute of each hyperlink
    hyperlinks = [link['href'] for link in links]

    # Print the list of hyperlinks
    print(hyperlinks)
else:
    # Print an error message if the request was not successful
    print('Error: Could not retrieve the page')

