import requests

class APIClient:
    def __init__(self, api_key: str, merchant_id: str, base_url: str):
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, data=None):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        url = f'{self.base_url}/{endpoint}'
        response = requests.request(method, url, headers=headers, json=data)

        if response.status_code != 201:
            # Will Handle errors here
            pass

        return response.json()

    def create_session(self, endpoint: str, request_data):
        response = self._make_request('POST', endpoint, data=request_data)
        return response
