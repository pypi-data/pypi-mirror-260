import os
import requests
from http import HTTPStatus
from typing import Optional
from urllib.parse import urljoin

from .base_code_block import BaseCodeBlock


class ConfigurationCodeBlock(BaseCodeBlock):
    """
    The ConfigurationCodeBlock provides access to configuration parameters set during creation.
    Any configured key is available through the get() method, returning the string value or raising an exception if no
    such configuration key exists.
    """

    def __init__(self, api_url="http://169.254.169.254:9000/secrets/v1/"):
        if 'BISMUTH_AUTH' not in os.environ:
            raise Exception("Missing BISMUTH_AUTH token in environment.")
        self.auth = {"Authorization": os.environ['BISMUTH_AUTH']}
        self.api_url = api_url

    def get(self, key) -> Optional[str]:
        resp = requests.get(urljoin(self.api_url, key), headers=self.auth)
        if resp.status_code == HTTPStatus.NOT_FOUND:
            raise AttributeError(f"Configuration key {key} not set")
        elif not resp.ok:
            raise Exception(f"Server error {resp}")
        return resp.text
