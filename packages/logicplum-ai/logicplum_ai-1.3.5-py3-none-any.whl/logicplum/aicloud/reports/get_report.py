import requests
import base64
import json
from ..config import base_url

def reports(deployment_id, token):
    url = f'{base_url}/plot/report'
    access_token = f'Bearer {token}'
    headers = {"Authorization": access_token}
    data = {"deployment_id": deployment_id}
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        pdf_data = base64.b64encode(response.content).decode('utf-8')
        return json.dumps({'result': pdf_data})
    except requests.exceptions.RequestException as e:
        return f"Failed to generate report: {e}"

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('/')[-1]  # Change '\\' to '/' for UNIX paths
        content = file.read()
        return uploaded_filename, content

def EDAreport(file_path, target, client_id, token):
    uploaded_filename, content = read_file(file_path)
    url = f"{base_url}/training/eda-report"
    data = {'target': target, 'client_id': client_id}
    files = {'file': (uploaded_filename, content)}
    access_token = f'Bearer {token}'
    headers = {"Authorization": access_token}
    
    try:
        response = requests.post(url, data=data, files=files, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Failed to generate EDA report: {e}"
