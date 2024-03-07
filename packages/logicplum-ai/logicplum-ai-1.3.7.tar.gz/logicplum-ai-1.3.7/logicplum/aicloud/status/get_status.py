import requests
from ..config import base_url, api_token

def make_request(url, token):
    access_token = 'Bearer ' + token
    headers = {"Authorization": access_token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the request fails
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_prediction_status(deployment_or_project_id, token, mode):
    url = f"{base_url}/prediction/check-prediction-status/{deployment_or_project_id}"
    return make_request(url, token)

def get_training_status(project_id, token):
    url = f"{base_url}/training/check-status/{project_id}"
    return make_request(url, token)
