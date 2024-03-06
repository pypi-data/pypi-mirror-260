import requests
from ..config import base_url, api_token

def create_account(name, email, username, password):
    url = f"{base_url}/client/"
    data = {
        "name": name,
        "email": email,
        "username": username,
        "password": password
    }
    headers = {"Authorization": api_token}
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Failed to create account: {e}"

def create_app(name, client_id, access_token):
    url = f"{base_url}/app/"
    data = {
        "name": name,
        "client": client_id
    }
    access_token = "Bearer " + access_token
    headers = {"Authorization": access_token}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Failed to create app: {e}"

def login(username, password):
    url = f"{base_url}/login"
    data = {
        "username": username,
        "password": password
    }
    headers = {"Authorization": api_token}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        output = response.json()
        try:
            del output["refresh"]
        except KeyError:
            pass
        return output
    except requests.exceptions.RequestException as e:
        return f"Failed to login: {e}"
