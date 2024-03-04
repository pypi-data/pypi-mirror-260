import requests

class Discover:

    def __init__(self,access_token:str, discover:dict) -> None:
        self.discover = discover
        self.access_token = access_token

    def call(self, method: str, endpoint: str, path: str, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        if not endpoint:
            raise ValueError("An endpoint must be provided.")

        if endpoint not in self.discover or 'path' not in self.discover[endpoint]:
            raise ValueError(f"endpoint '{endpoint}' not found")
        
        x_api_key = self.discover[endpoint].get("key", "")
        full_path = f"{self.discover[endpoint]['path']}{path}"
        full_headers = {"Authorization": self.access_token}
        if x_api_key:
            full_headers["x-api-key"] = x_api_key

        if headers:
            full_headers.update(headers)

        request_func = getattr(requests, method.lower())
        response = request_func(full_path, params=params, headers=full_headers, json=data)

        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            print(f"HTTP Status Code: {errh.response.status_code}")
            print(f"Response Text: {errh.response.text}")
            print(f"Request URL: {errh.request.url}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

        return {}

    def get(self, endpoint, path: str, params: dict = None, headers: dict = None) -> dict:
        return self.call("GET", endpoint, path, params=params, headers=headers)

    def post(self, endpoint, path: str, data: dict = None, params: dict = None, headers: dict = None) -> dict:
        return self.call("POST", endpoint, path, params=params, headers=headers, data=data)

    def put(self, endpoint, path: str, data: dict = None, params: dict = None, headers: dict = None) -> dict:
        return self.call("PUT", endpoint, path, params=params, headers=headers, data=data)

    def delete(self, endpoint, path: str, params: dict = None, headers: dict = None) -> dict:
        return self.call("DELETE", endpoint, path, params=params, headers=headers)
