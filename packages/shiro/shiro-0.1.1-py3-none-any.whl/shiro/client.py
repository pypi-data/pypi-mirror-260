import requests
from .deployment import Deployment
from .prompt import Prompt

class ShiroClient:
    def __init__(self, api_key):
        if api_key is None:
            raise ValueError("API key not defined")
        self.api_key = api_key
        self.base_url = "https://openshiro.com/api/v1"
        self.deployments = Deployment(self)
        self.prompts = Prompt(self)

    def request(self, method, path, data=None):
        url = f"{self.base_url}/{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, url, json=data, headers=headers)
        return response.json()
