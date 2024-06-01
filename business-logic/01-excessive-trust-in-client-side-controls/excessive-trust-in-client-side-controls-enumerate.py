from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Specify Variables
base_url = "https://0a1f00410450ba6680aa8a200085007a.web-security-academy.net"
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Parse Base URL
content = BeautifulSoup(requests.get(base_url).text, 'html.parser')

# Find and Request all href resource
for link in content.find_all('a', href=True):
  full_url = urljoin(base_url,link['href'])
  response = requests.get(full_url, proxies=proxies, verify=False)
  print(f"{response.status_code} {response.url}")

# Find and Request all src resource
for img in content.find_all('img', src=True):
  full_url = urljoin(base_url,img['src'])
  response = requests.get(full_url, proxies=proxies, verify=False)
  print(f"{response.status_code} {response.url}")