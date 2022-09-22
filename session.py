import json
import requests
from requests import RequestException
from requests.auth import HTTPBasicAuth
from logger import Logger


class HTTPSession:
    URL = 'http://127.0.0.1:8080/'

    @staticmethod
    def register_user_request(request_type, endpoint, params):
        do_logging = params.pop('do_logging', True)
        try:
            response = request_type(endpoint, params)
            if do_logging:
                Logger.log_request(request_type, endpoint, params, response.status_code)
            return response.status_code
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))

    @staticmethod
    def get_users_request(request_type, endpoint):
        try:
            response = request_type(endpoint)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))

    @staticmethod
    def get_auth_token_request(request_type, endpoint, username, password):
        try:
            response = request_type(endpoint, auth=HTTPBasicAuth(username, password))
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))

    @staticmethod
    def get_user_request(request_type, endpoint, token):
        header = {"Token": token}
        try:
            response = request_type(endpoint, headers=header)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))

    @staticmethod
    def update_user_request(request_type, endpoint, token, body):
        headers = {"Token": token, 'Content-type': 'application/json'}
        try:
            response = request_type(endpoint, headers=headers, data=body)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))


class RequestTypes:
    GET = requests.get
    POST = requests.post
    PUT = requests.put


class Endpoints:
    REGISTER = HTTPSession.URL + 'register'
    GET_USERS = HTTPSession.URL + 'api/users'
    GET_AUTH_TOKEN = HTTPSession.URL + 'api/auth/token'
    GET_USER = HTTPSession.URL + 'api/users/'
    UPDATE_USER = HTTPSession.URL + 'api/users/'


class StatusCodes:
    STATUS_200 = '200'
    STATUS_201 = '201'
