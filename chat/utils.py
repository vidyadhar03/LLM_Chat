# chat/utils.py
import requests
from django.conf import settings

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/"

HEADERS = {
    "Authorization": f"Bearer {settings.HUGGING_FACE_API_TOKEN}"
}

def get_huggingface_response(model_name, prompt):
    url = f"{HUGGING_FACE_API_URL}{model_name}"
    response = requests.post(url, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Error: Unable to fetch response from the model."
