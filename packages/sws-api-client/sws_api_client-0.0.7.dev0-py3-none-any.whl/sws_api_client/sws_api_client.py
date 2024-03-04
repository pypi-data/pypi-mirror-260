import argparse
import json
import os

from typing import Optional

import requests

from sws_api_client.discover import Discover

class SwsApiClient:

    def __init__(self, sws_endpoint: str, access_token: str, current_task_id:Optional[str], current_execution_id:Optional[str] ) -> None:
        self.sws_endpoint = sws_endpoint
        self.access_token = access_token
        self.current_task_id = current_task_id
        self.current_execution_id = current_execution_id
        self.discover = self.__get_discover()
        self.is_debug = self.check_debug()
        self.discoverable = Discover(self.access_token, self.discover)

    def __get_discover(self) -> dict:
        discover_endpoint = f"{self.sws_endpoint}/discover?v=2"
        headers = {"Authorization": self.access_token}
        return requests.get(url=discover_endpoint, headers=headers).json()

    @classmethod
    def from_env(cls, sws_endpoint_env="SWS_ENDPOINT", access_token_env="ACCESS_TOKEN"):
        return cls(
            sws_endpoint=os.getenv(sws_endpoint_env),
            access_token=os.getenv(access_token_env),
            current_task_id = os.getenv("TASK_ID"),
            current_execution_id = os.getenv("EXECUTION_ID")
        )

    @classmethod
    def from_conf(cls, conf_file="conf_sws_api_client.json"):
        with open(conf_file) as f:
            kwargs = json.load(f)
            return cls(**kwargs)

    @classmethod
    def from_args(cls):
        parser = argparse.ArgumentParser(
            description="Instantiate SwsApiClient from args"
        )
        parser.add_argument(
            "--sws_endpoint", type=str, required=True, help="The sws endpoint"
        )
        parser.add_argument(
            "--access_token", type=str, required=True, help="The access token"
        )
        parser.add_argument(
            "--current_task_id", type=str, required=False, help="The current task ID"
        )
        parser.add_argument(
            "--current_execution_id", type=str, required=False, help="The current execution ID"
        )

        args, _ = parser.parse_known_args()

        return cls(**vars(args))
    
    @classmethod
    def check_debug(self):
        return os.getenv("DEBUG_MODE") == "TRUE" or os.getenv("DEBUG_MODE") is None
    
    @classmethod
    def auto(cls):
        debug = cls.check_debug()
        if debug:
            return cls.from_conf()
        else:
            return cls.from_env()


    def get_dataset_export_details(self, dataset_id: str) -> dict:

        session_api_key = self.discover["session_api"]["key"]
        session_api_path = self.discover["session_api"]["path"]

        url = f"{session_api_path}/dataset/{dataset_id}/info"
        params = {"extended": "true"}
        headers = {"Authorization": self.access_token, "x-api-key": session_api_key}

        response = requests.get(url, params=params, headers=headers).json()

        return response

    def get_read_access_url(self, path: str, expiration: int) -> dict:

        tag_api_key = self.discover["tag_api"]["key"]
        tag_api_path = self.discover["tag_api"]["path"]

        url = f"{tag_api_path}/tags/dissemination/getReadAccessUrl"
        body = {"path": path, "expiration": expiration}
        headers = {"Authorization": self.access_token, "x-api-key": tag_api_key}

        response = requests.post(url, json=body, headers=headers).json()

        return response
