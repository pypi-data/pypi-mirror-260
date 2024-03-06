# Python Imports
import requests

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import


class MicroserviceClient:
    """A client for interacting with a microservice via HTTP requests."""

    def __init__(self, tenant_identifier=None, token=None,url=None,headers=None):
        """Initialize the MicroserviceClient instance."""
        self.tenant_identifier = tenant_identifier
        self.token = token
        self.url = url
        self.headers = headers

    def make_request(self, method, data=None, params=None):
        """Make an HTTP request to the specified endpoint with the given method."""
        request_method = getattr(requests, method.lower())
        response = request_method(self.url, json=data, headers=self.headers, params=params,timeout=30)
        return response

    def post(self, data=None, params=None):
        """Make an HTTP POST request to the specified"""
        return self.make_request('POST', data=data, params=params)

    def get(self, params=None):
        """Make an HTTP GET request to the specified"""
        return self.make_request('GET', params=params)

    def patch(self, data=None, params=None):
        """Make an HTTP PATCH request to the specified"""
        return self.make_request('PATCH', data=data, params=params)

    def put(self, data=None, params=None):
        """Make an HTTP PUT request to the specified"""
        return self.make_request('PUT', data=data, params=params)

