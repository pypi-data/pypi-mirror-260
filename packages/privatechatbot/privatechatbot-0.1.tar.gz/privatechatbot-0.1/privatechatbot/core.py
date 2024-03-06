import requests
import json
# import time

class PrivateChatbot:
    def __init__(self, api_key):
        self.API_BASE_URL = 'http://localhost:5000'
        # self.API_BASE_URL = 'https://api.anote.ai'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    def upload(self, file_paths, task_type, model_type):
        url = f"{self.API_BASE_URL}/public/upload"
        data = {
            "task_type": task_type,
            "model_type": model_type
        }
        # Open the files in binary mode and include them in a dictionary
        files_dict = {path: open(path, 'rb') for path in file_paths}
        response = requests.post(url, data=data, files=files_dict, headers=self.headers)
        # Close the files after sending
        for file in files_dict.values():
            file.close()
        return response.json()

    def chat(self, dataset_id, text):
        url = f"{self.API_BASE_URL}/public/chat"
        data = json.dumps({
            "id": dataset_id,
            "text": text
        })
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    def evaluate(self, dataset_id):
        """
        Evaluate predictions on one or multiple documents/text.
        :param dataset_id: The ID of the dataset that has had predictions made on it.
        """
        if not dataset_id:
            return {"error": "Dataset ID is not set. Please create a dataset first."}

        url = f"{self.API_BASE_URL}/public/evaluate"
        # For file uploads, requests can handle files directly in the 'files' parameter

        data = {'datasetId': dataset_id} #'task_type': task_type}  # Infer task type for now
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()