import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

types = ['text', 'password', 'email', 'search', 'url', 'tel', 'number', 'hidden', 'date', 'datetime-local', 'month', 'week', 'time']

def fetch_forms_inputs(target_url):
    inputs_info = []
    print("Starting Inputs Scanner..")
    try:
        response = requests.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        forms = soup.find_all('form')
        if not forms:
            print("No forms found on the page.")
            return []

        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            full_url = urljoin(target_url, action) if action else target_url

            inputs = form.find_all('input')
            data = []
            for input_tag in inputs:
                name = input_tag.get('name')
                input_type = input_tag.get('type', 'text')
                if name and input_type in types:
                    data.append(name)
            if data:
                inputs_info.append({'url': full_url, 'method': method, 'params': data})

        return inputs_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

