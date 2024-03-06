import os
import requests

def embed():
    return "test"

def chat_completion(model_params):
    api_key = os.environ.get('SIGIQ_API_KEY')
    exp_name = os.environ.get('SIGIQ_EXP_NAME')
    
    url = "http://35.247.56.152/call-gpt/"

    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "api_key": api_key,
        "exp_name": exp_name,
        "model_params": model_params,
    }

    response = requests.get(url, json=payload, headers=headers)
    return response

def get_stats(user=None, exp_name=None):
    api_key = os.environ.get('SIGIQ_API_KEY')
    
    url = "http://35.247.56.152/get-stats/"
    
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "api_key": api_key,
        "exp_name": exp_name,
    }
    if user:
        payload['user'] = user

    response = requests.get(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.text
        return f"Request failed with status code {response.status_code}: {error_message}"
