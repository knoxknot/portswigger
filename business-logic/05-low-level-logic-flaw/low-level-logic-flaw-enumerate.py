from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://0a4c001e030d58a4847c65e80013002f.web-security-academy.net"
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
content = BeautifulSoup(requests.get(base_url).text, 'html.parser')
for link in content.find_all('a', href=True):
  full_url = urljoin(base_url,link['href'])
  response = requests.get(full_url, proxies=proxies, verify=False)
  print(f"{response.status_code} {response.url}")
for img in content.find_all('img', src=True):
  full_url = urljoin(base_url,img['src'])
  response = requests.get(full_url, proxies=proxies, verify=False)
  print(f"{response.status_code} {response.url}")