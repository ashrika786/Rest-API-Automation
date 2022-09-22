from datetime import timedelta
from time import time
from logger import Logger


def decorate_test(test_function):
    def wrapper():
        Logger.log_test_start(test_function)
        time_delta, _ = measure_time(test_function)
        Logger.log_test_finish(test_function, timedelta(seconds=time_delta))

    return wrapper


def measure_time(function):
    start = time()
    result = function()
    end = time()
    return end - start, result


class Constants:
    payload = 'payload'
    username_value = 'TestUser'
    password_value = '1234'
    firstname_value = 'Test'
    lastname_value = 'User'
    phone_value = '123456789'

class RequestParams:
    username_key = 'username'
    password_key = 'password'
    firstname_key = 'firstname'
    lastname_key = 'lastname'
    phone_key = 'phone'
    token_key = 'token'
    status_key = 'status'
    payload_key = 'payload'
    success_key = 'SUCCESS'

