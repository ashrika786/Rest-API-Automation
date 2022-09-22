from asserter import assert_true, assert_equal
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test, Constants, RequestParams
import json

REGISTER_ENDPOINT = Endpoints.REGISTER
GET_USERS_ENDPOINT = Endpoints.GET_USERS
GET_AUTH_TOKEN_ENDPOINT = Endpoints.GET_AUTH_TOKEN
GET_USER_ENDPOINT = Endpoints.GET_USER
UPDATE_USER_ENDPOINT = Endpoints.UPDATE_USER

registerApiParams = {RequestParams.username_key: Constants.username_value,
                     RequestParams.password_key: Constants.password_value,
                     RequestParams.firstname_key: Constants.firstname_value,
                     RequestParams.lastname_key: Constants.lastname_value,
                     RequestParams.phone_key: Constants.phone_value}

class Auth:

    @staticmethod
    def return_auth_token():
        status_code, auth_data = HTTPSession.get_auth_token_request(RequestTypes.GET, GET_AUTH_TOKEN_ENDPOINT,
                                                                    Constants.username_value,
                                                                    Constants.password_value)
        return auth_data[RequestParams.token_key]

class UserData:

    @staticmethod
    def read_user_data(file_name):
        with open(file_name, 'r') as openfile:
            return json.load(openfile)

    @staticmethod
    def Merge(dict1, dict2):
        return dict1.update(dict2)

    @staticmethod
    def update_user_data(file_name, update_object):
        current_object = UserData.read_user_data(file_name)
        UserData.Merge(current_object, update_object)
        json_object = json.dumps(current_object, indent=4)

        # Writing to sample.json
        print(current_object)
        with open(file_name, "w") as outfile:
            outfile.write(json_object)

class TestDemoApp:

    @staticmethod
    @decorate_test
    def test_demo_app_register_api_status_code():
        status_code = HTTPSession.register_user_request(RequestTypes.POST, REGISTER_ENDPOINT, registerApiParams)
        assert_equal(status_code, StatusCodes.STATUS_200, f'Status code of {REGISTER_ENDPOINT} endpoint')

    @staticmethod
    @decorate_test
    def test_demo_get_users_data():
        _, response_data = HTTPSession.get_users_request(RequestTypes.GET, GET_USERS_ENDPOINT)
        assert_true(Constants.username_value in response_data[Constants.payload],
                    "Yes " + Constants.username_value + " found in List")

    @staticmethod
    @decorate_test
    def test_demo_get_auth_token():
        token = Auth.return_auth_token()
        status_code, response_data = HTTPSession.get_user_request(RequestTypes.GET,
                                                                  GET_USER_ENDPOINT + Constants.username_value,
                                                                  token)
        user = UserData.read_user_data("user_data.json")

        assert_equal(status_code, StatusCodes.STATUS_200,
                     f'Status code of {GET_USER_ENDPOINT + Constants.username_value} endpoint')

        assert_equal(response_data[RequestParams.status_key], RequestParams.success_key,
                     'User data have "Status" Value where')

        assert_equal(response_data[RequestParams.payload_key][RequestParams.firstname_key], user["firstname"],
                     'User data have "First Name" Value where')

        assert_equal(response_data[RequestParams.payload_key][RequestParams.lastname_key], user["lastname"],
                     'User data have "Last Name" Value where')

        assert_equal(response_data[RequestParams.payload_key][RequestParams.phone_key], user["phone"],
                     'User data have "Phone Number" Value where')

    @staticmethod
    @decorate_test
    def test_demo_update_user_data():
        token = Auth.return_auth_token()
        dictionary = {
            "firstname": "Test2",
            "lastname": "User2",
            "phone": "123"
        }

        UserData.update_user_data("user_data.json",dictionary)
        status_code, response_data = HTTPSession.update_user_request(RequestTypes.PUT,
                                                                     UPDATE_USER_ENDPOINT + Constants.username_value,
                                                                     token, json.dumps(dictionary))
        assert_equal(status_code, StatusCodes.STATUS_201,
                     f'Status code of {UPDATE_USER_ENDPOINT + Constants.username_value} endpoint')
