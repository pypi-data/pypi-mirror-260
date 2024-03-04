from sws_api_client.sws_api_client import SwsApiClient

class Datasets:

    def __init__(self, sws_client: SwsApiClient) -> None:
        self.sws_client = sws_client

    def get_dataset_export_details(self, dataset_id: str) -> dict:

        url = f"/dataset/{dataset_id}/info"
        params = {"extended": "true"}

        response = self.sws_client.discoverable.get('session_api', url, params=params)

        return response