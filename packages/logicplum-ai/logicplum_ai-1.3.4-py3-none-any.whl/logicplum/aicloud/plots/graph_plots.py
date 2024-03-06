import requests
import json
import io
from PIL import Image as PilImage
from ..config import base_url

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('/')[-1]
        content = file.read()
        return uploaded_filename, content

def make_request(url, data, token):
    access_token = f'Bearer {token}'
    headers = {"Authorization": access_token}
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def display_response(res_type, response):
    if res_type == 'base64':
        return response
    else:
        if isinstance(response, bytes) and (response.startswith(b'\x89PNG') or response.startswith(b'\xff\xd8\xff\xe0')):
            image = PilImage.open(io.BytesIO(response))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            return image
        else:
            response_dict = json.loads(response.decode('utf-8'))
            return response_dict

def plot_api_request(endpoint, deployment_id, res_type, token):
    data = {
        "deployment_id": deployment_id,
        "res_type": res_type 
    }
    url = f"{base_url}/plot/{endpoint}"
    response = make_request(url, data, token)
    if response:
        if data['res_type'] == 'image':
            return response.content
        return response.json()
    return None

def roc_plot(deployment_id, res_type, token):
    return plot_api_request("roc", deployment_id, res_type, token)

def advanced_lift_chart(deployment_id, res_type, token):
    return plot_api_request("advanced-lift-chart", deployment_id, res_type, token)

def advanced_feature_impact(deployment_id, res_type, token):
    return plot_api_request("advanced-feature-impact", deployment_id, res_type, token)

def partial_dependency(deployment_id, res_type, token):
    return plot_api_request("partial-dependency", deployment_id, res_type, token)

def residual(deployment_id, res_type, token):
    return plot_api_request("residual", deployment_id, res_type, token)

def predict_vs_actual(deployment_id, res_type, token):
    return plot_api_request("predict-vs-actual", deployment_id, res_type, token)

def word_cloud(deployment_id, res_type, token):
    return plot_api_request("wordcloud", deployment_id, res_type, token)

def confusion_matrix(deployment_id, res_type, token):
    return plot_api_request("confusion-matrix", deployment_id, res_type, token)

def get_all_columns(deployment_id, token, n_features):
    if n_features <= 10:
        return None, "Number of features should be greater than 10"

    url = f"{base_url}/plot/dataset-columns"
    data = {
        "deployment_id": deployment_id,
        "n_features": n_features
    }
    response = make_request(url, data, token)
    if response:
        return response.json()
    return None, None

def prediction_distribution(deployment_id, res_type, token):
    return plot_api_request("prediction-distribution", deployment_id, res_type, token)

def blueprint_plot(deployment_id, token):
    data = {"deployment_id": deployment_id}
    url = f"{base_url}/plot/blueprint-plot"
    response = make_request(url, data, token)
    if response:
        return response.json()
    return None
