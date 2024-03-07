#
# PlasmaPlatformClient
# Copyright (c) 2024 10xDevelopment LLC
#

import requests
import base64

class RESTClient:
    def __init__(self, base_url, access_token, access_token_type, default_headers = {}):
        # Remove any trailing slashes...
        base_url = base_url.rstrip('/')

        self.base_url = base_url
        self.access_token = access_token
        self.access_token_type = access_token_type
        self.default_headers = default_headers
        self.verify_ssl = False

    # Initialize the client with no auth...
    @staticmethod
    def for_no_auth(base_url):
        return RESTClient(base_url, None, None)

    # Initialize the client with a Bearer token...
    @staticmethod
    def for_bearer_token(base_url, access_token):
        return RESTClient(base_url, access_token, "Bearer")

    # Initialize the client for Basic Auth...
    @staticmethod
    def for_basic_auth(base_url, user, pwd):
        # Create the access token by combining user/pwd...
        access_token = user + ':' + pwd
        access_token = base64.b64encode(access_token.encode('utf-8')).decode('utf-8')
        return RESTClient(base_url, access_token, "Basic")

    # Get the authorization header for this instance...
    def __get_auth_header(self):
        # Check if token or type is None...
        if (not self.access_token) or (not self.access_token_type):
            return None
        return self.access_token_type + ' ' + self.access_token

    # Adds all headers, including (1) default headers, (2) auth header, (3) any additional headers...
    def __get_all_headers(self, addl_headers):
        headers = {}

        # Default headers...
        if self.default_headers:
            headers.update(self.default_headers)

        # Auth header...
        if self.access_token and self.access_token_type:
            headers['Authorization'] = self.__get_auth_header()

        # Additional headers...
        if addl_headers:
            headers.update(addl_headers)

        return headers

    # GET
    def get(self, url, params = {}, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.get(url, params, headers=headers, verify=self.verify_ssl)

    # GET, returning JSON
    def get_json(self, url, params = {}, addl_headers = {}):
        response = self.get(url, params, addl_headers)
        return response.json()

    # POST
    def post(self, url, data, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.post(url, data, headers=headers, verify=self.verify_ssl)

    # POST, returning JSON
    def post_json(self, url, data, addl_headers = {}):
        response = self.post(url, data, addl_headers)
        return response.json()

    # PUT
    def put(self, url, data, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.put(url, data, headers=headers, verify=self.verify_ssl)

    # PUT, returning JSON
    def put_json(self, url, data, addl_headers = {}):
        response = self.put(url, data, addl_headers)
        return response.json()

    # DELETE
    def delete(self, url, addl_headers = {}):
        headers = self.__get_all_headers(addl_headers)
        return requests.delete(url, headers=headers, verify=self.verify_ssl)

    # DELETE, returning JSON
    def delete_json(self, url, addl_headers = {}):
        response = self.delete(url, addl_headers)
        return response.json()
