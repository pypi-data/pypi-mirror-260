# account_api.py

import requests
import json
from .utils import m5_signature, status_code

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

    def get_accounts(self):
        """
        Retrieves details of a single account.

        Args:
            account_id (str): The ID of the account to retrieve.

        Returns:
            dict: Account details.
        """
        endpoint = f'{self.base_url}apiv2/account'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.get(full_url)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    # def create_account(self, account_data):
    #     """
    #     Outdated
    #     Creates a new sub-account.

    #     Args:
    #         account_data (dict): Data for creating the account.

    #     Returns:
    #         dict: Response data.
    #     """
    #     endpoint = f'{self.base_url}apiv2/account'
    #     params = {'apiKey':self.api_key}
    #     api_sign = m5_signature(self.api_key, self.secret, params)
    #     full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
    #     response = requests.post(full_url, json=account_data)
    #     exit = status_code(response.status_code)
    #     if exit['result']:
    #         return response.json()
    #     else:
    #         return exit

    # Add other methods for managing account-related operations
