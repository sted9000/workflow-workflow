import requests
import os
from dotenv import load_dotenv

load_dotenv()

class n8nApiRequestService:
    
    def __init__(self):
        self.api_key = os.getenv("N8N_API_KEY")
        self.n8n_url = "https://n8n-server-production.up.railway.app/api/v1/workflows"
        self.headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }

    def create_workflow(self, workflow_data):
        try:
            print(self.headers)
            response = requests.post(self.n8n_url, headers=self.headers, json=workflow_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating workflow: {e}")
