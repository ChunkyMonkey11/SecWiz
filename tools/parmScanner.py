import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config.config import TYPES
urls =['http://testphp.vulnweb.com/signup.php','http://testphp.vulnweb.com/guestbook.php', 'http://testphp.vulnweb.com/login.php']
url = 'http://testphp.vulnweb.com/login.php'

def fetch_forms_inputs(target_url):
    inputs_info = []
    print("Starting Inputs Scanner..")
    for target in target_url:
        try:
            response = requests.get(target)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            forms = soup.find_all('form')
            if not forms:
                print("No forms found on the page.")
                pass

            for form in forms:
                action = form.get('action')
                method = form.get('method', 'get').lower()
                full_url = urljoin(target, action) if action else target
                inputs = form.find_all('input')
                data = []
                for input_tag in inputs:
                    name = input_tag.get('name')
                    input_type = input_tag.get('type', 'text')
                    if name and input_type in TYPES:
                        data.append(name)
                if data:
                    new = {'url': full_url, 'method': method, 'params': data}
                    if new not in inputs_info:
                        inputs_info.append(new)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return []
    return inputs_info
