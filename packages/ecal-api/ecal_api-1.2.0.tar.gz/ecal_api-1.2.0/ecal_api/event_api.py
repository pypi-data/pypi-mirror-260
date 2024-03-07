# event_api.py

import requests
import json
from .utils import m5_signature

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

    def get_events(self, params):
        """
        Get a list of events.

        Args:
            params (dict): Parameters for filtering events.

        Returns:
            dict: Response containing a list of events.
        """
        endpoint = f'{self.base_url}/apiv2/event/'
        params['apiKey'] = self.api_key
        params['apiSign'] = m5_signature(params)
        response = requests.get(endpoint, params=params)
        return response.json()

    def get_event(self, event_id, params=None):
        """
        Get details of a single event.

        Args:
            event_id (str): The ID of the event.
            params (dict, optional): Additional parameters.

        Returns:
            dict: Details of the event.
        """
        endpoint = f'{self.base_url}/apiv2/event/{event_id}'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        params['apiSign'] = m5_signature(params)
        response = requests.get(endpoint, params=params)
        return response.json()

    def create_event(self, event_data):
        """
        Create a new event.

        Args:
            event_data (dict): Data for creating the event.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/event/'
        event_data['apiKey'] = self.api_key
        event_data['apiSign'] = m5_signature(event_data)
        response = requests.post(endpoint, json=event_data)
        return response.json()

    def update_event(self, event_id, event_data):
        """
        Update an existing event.

        Args:
            event_id (str): The ID of the event to update.
            event_data (dict): Updated event data.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/event/{event_id}'
        event_data['apiKey'] = self.api_key
        event_data['apiSign'] = m5_signature(event_data)
        response = requests.put(endpoint, json=event_data)
        return response.json()

    def delete_event(self, event_id):
        """
        Delete an event.

        Args:
            event_id (str): The ID of the event to delete.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/event/{event_id}'
        params = {'apiKey': self.api_key, 'apiSign': m5_signature({'apiKey': self.api_key})}
        response = requests.delete(endpoint, params=params)
        return response.json()
