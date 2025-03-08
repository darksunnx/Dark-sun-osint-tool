import requests

class LeakOSINTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://leakosint.com/api/v1"
    
    def search(self, search_type, query):
        if not self.api_key:
            raise Exception("API key not configured")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        endpoint = f"{self.base_url}/search/{search_type}"
        
        try:
            response = requests.get(
                endpoint,
                params={"query": query},
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
