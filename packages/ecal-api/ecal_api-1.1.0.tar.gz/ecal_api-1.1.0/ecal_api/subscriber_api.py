# subscriber_api.py

import requests
import json
from utils import m5_signature

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
        endpoint = f'{self.base_url}/apiv2/subscriber/{subscriber_id}'
        params = {'apiKey': self.api_key}
        api_sign = m5_signature(params, self.secret)
        params['apiSign'] = api_sign
        response = requests.get(endpoint, params=params)
        return response.json()

    def get_subscription(self, email_address):
        """
        Get subscription details by email address.

        Args:
            email_address (str): The email address of the subscriber.

        Returns:
            dict: Details of the subscription.
        """
        endpoint = f'{self.base_url}/apiv2/subscriber/{email_address}'
        params = {'apiKey': self.api_key}
        api_sign = m5_signature(params, self.secret)
        params['apiSign'] = api_sign
        response = requests.get(endpoint, params=params)
        return response.json()
