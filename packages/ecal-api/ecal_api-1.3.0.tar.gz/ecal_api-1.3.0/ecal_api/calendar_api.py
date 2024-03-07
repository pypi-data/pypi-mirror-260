# calendar_api.py

import requests
import json
from .utils import m5_signature, status_code

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

    def get_calendars(self, params={}):
        """
        Get a list of calendars.

        Args:
            params (dict, optional): Additional parameters as a dictionary.

        Returns:
            dict: Response containing a list of calendars.
        """
        endpoint = f'{self.base_url}apiv2/calendar/'
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.get(full_url)
        exit = status_code( response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def get_calendar(self, calendar_id, params=None):
        """
        Get details of a single calendar.

        Args:
            calendar_id (str): The ID of the calendar.
            params (dict, optional): Additional parameters.

        Returns:
            dict: Details of the calendar.
        """
        endpoint = f'{self.base_url}apiv2/calendar/{calendar_id}'
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

    def create_calendar(self, calendar_data):
        """
        Create a new calendar.

        Args:
            calendar_data (dict): Data for creating the calendar.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/calendar'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.post(full_url, json=calendar_data)
        exit = status_code( response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def update_calendar(self, calendar_id, calendar_data):
        """
        Update an existing calendar.

        Args:
            calendar_id (str): The ID of the calendar to update.
            calendar_data (dict): Updated calendar data.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/calendar/{calendar_id}'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.put(full_url, json=calendar_data)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit

    def delete_calendar(self, calendar_id):
        """
        Delete a calendar.

        Args:
            calendar_id (str): The ID of the calendar to delete.

        Returns:
            dict: Response data.
        """
        endpoint = f'{self.base_url}apiv2/calendar/{calendar_id}'
        params = {'apiKey':self.api_key}
        api_sign = m5_signature(self.api_key, self.secret, params)
        full_url = endpoint + '?' + '&'.join([f"{key}={value}" for key, value in params.items()]) + f'&apiSign={api_sign}'
        response = requests.delete(full_url)
        exit = status_code(response.status_code)
        if exit['result']:
            return response.json()
        else:
            return exit
