# subscriber_api.py

import requests
import json
from .utils import m5_signature, status_code

class SubscriberAPI:
    def __init__(self, api_key, secret):
        """
        Initialize the SubscriberAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_subscriber(self, subscriber_id):
        """
        Get details of a single subscriber.

        Args:
            subscriber_id (str): The ID of the subscriber.

        Returns:
            dict: Details of the subscriber.
        """
        endpoint = f'{self.base_url}apiv2/subscriber/{subscriber_id}'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.get(full_url)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def get_subscription(self, email_address):
        """
        Get subscription details by email address.

        Args:
            email_address (str): The email address of the subscriber.

        Returns:
            dict: Details of the subscription.
        """
        endpoint = f'{self.base_url}apiv2/subscriber/{email_address}'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.get(full_url)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit
