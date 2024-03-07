# account_api.py

import requests
import json
from .utils import m5_signature

class AccountAPI:
    def __init__(self, api_key, secret):
        """
        Initializes the AccountAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_account(self, account_id):
        """
        Retrieves details of a single account.

        Args:
            account_id (str): The ID of the account to retrieve.

        Returns:
            dict: Account details.
        """
        endpoint = f'{self.base_url}/apiv2/account/{account_id}'
        params = {
            'apiKey': self.api_key,
            'apiSign': m5_signature({'apiKey': self.api_key, 'apiSign': self.secret})
        }
        response = requests.get(endpoint, params=params)
        return response.json()

    def create_account(self, account_data):
        """
        Creates a new sub-account.

        Args:
            account_data (dict): Data for creating the account.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/account'
        params = {
            'apiKey': self.api_key,
            'apiSign': m5_signature({'apiKey': self.api_key, 'apiSign': self.secret})
        }
        response = requests.post(endpoint, params=params, json=account_data)
        return response.json()

    # Add other methods for managing account-related operations
