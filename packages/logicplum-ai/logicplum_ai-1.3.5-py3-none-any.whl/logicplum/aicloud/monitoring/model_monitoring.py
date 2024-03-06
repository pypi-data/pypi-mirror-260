import requests
from ..config import base_url

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('/')[-1]
        content = file.read()
        return uploaded_filename, content

def monitor_model(token, deployment_id, res_type, file_path, mode, modelling_mode):
    data = {
        'res_type': res_type,
        'deployment_id': deployment_id
    }
    
    if modelling_mode.lower() == 'aipilot':
        url = f"{base_url}/training/aipilot/monitor-model"
    elif modelling_mode.lower() == 'comprehensive':
        url = f"{base_url}/training/comprehensive/monitor-model"
    else:
        return "Invalid mode!"

    access_token = 'Bearer ' + token
    headers = {"Authorization": access_token}
    uploaded_filename, content = read_file(file_path)
    files = {'file': (uploaded_filename, content)}

    try:
        response = requests.post(url, data=data, headers=headers, files=files)
        response.raise_for_status()
        response_json = response.json()
        
        if response_json['modelling_mode'].lower() == mode:
            if res_type == 'image':
                return response.content
            return response_json['result']
        else:
            return "Invalid Mode!"
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
