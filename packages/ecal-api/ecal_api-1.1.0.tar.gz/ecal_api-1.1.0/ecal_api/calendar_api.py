# calendar_api.py

import requests
import json
from utils import m5_signature

class CalendarAPI:
    def __init__(self, api_key, secret):
        """
        Initialize the CalendarAPI object with API key and secret.

        Args:
            api_key (str): The API key provided by ECAL.
            secret (str): The secret key for signing requests.
        """
        self.api_key = api_key
        self.secret = secret
        self.base_url = 'https://api.ecal.com/'

    def get_calendars(self, params=None):
        """
        Get a list of calendars.

        Args:
            params (dict, optional): Additional parameters.

        Returns:
            dict: Response containing a list of calendars.
        """
        endpoint = f'{self.base_url}/apiv2/calendar/'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        params['apiSign'] = m5_signature(params)
        response = requests.get(endpoint, params=params)
        return response.json()

    def get_calendar(self, calendar_id, params=None):
        """
        Get details of a single calendar.

        Args:
            calendar_id (str): The ID of the calendar.
            params (dict, optional): Additional parameters.

        Returns:
            dict: Details of the calendar.
        """
        endpoint = f'{self.base_url}/apiv2/calendar/{calendar_id}'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        params['apiSign'] = m5_signature(params)
        response = requests.get(endpoint, params=params)
        return response.json()

    def create_calendar(self, calendar_data):
        """
        Create a new calendar.

        Args:
            calendar_data (dict): Data for creating the calendar.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/calendar/'
        calendar_data['apiKey'] = self.api_key
        calendar_data['apiSign'] = m5_signature(calendar_data)
        response = requests.post(endpoint, json=calendar_data)
        return response.json()

    def update_calendar(self, calendar_id, calendar_data):
        """
        Update an existing calendar.

        Args:
            calendar_id (str): The ID of the calendar to update.
            calendar_data (dict): Updated calendar data.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/calendar/{calendar_id}'
        calendar_data['apiKey'] = self.api_key
        calendar_data['apiSign'] = m5_signature(calendar_data)
        response = requests.put(endpoint, json=calendar_data)
        return response.json()

    def delete_calendar(self, calendar_id):
        """
        Delete a calendar.

        Args:
            calendar_id (str): The ID of the calendar to delete.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}/apiv2/calendar/{calendar_id}'
        params = {'apiKey': self.api_key, 'apiSign': m5_signature({'apiKey': self.api_key})}
        response = requests.delete(endpoint, params=params)
        return response.json()
