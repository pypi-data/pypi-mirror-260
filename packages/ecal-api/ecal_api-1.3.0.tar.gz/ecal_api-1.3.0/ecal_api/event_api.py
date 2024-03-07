# event_api.py

import requests
import json
from .utils import m5_signature, status_code

class EventAPI:
    def __init__(self, api_key, secret):
        """
        Initialize the EventAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_events(self, params=None):
        """
        Get a list of events.

        Args:
            params (dict): Parameters for filtering events.

        Returns:
            dict: Response containing a list of events.
        """
        endpoint = f'{self.base_url}apiv2/event'
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

    def get_event(self, event_id, params=None):
        """
        Get details of a single event.

        Args:
            event_id (str): The ID of the event.
            params (dict, optional): Additional parameters.

        Returns:
            dict: Details of the event.
        """
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
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

    def create_event(self, event_data):
        """
        Create a new event.

        Args:
            event_data (dict): Data for creating the event.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/event/'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.post(full_url, json=event_data)
        exit = status_code( response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def update_event(self, event_id, event_data):
        """
        Update an existing event.

        Args:
            event_id (str): The ID of the event to update.
            event_data (dict): Updated event data.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.put(full_url, json=event_data)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def delete_event(self, event_id):
        """
        Delete an event.

        Args:
            event_id (str): The ID of the event to delete.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/event/{event_id}'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.delete(full_url)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit
