import requests
from flask import request, current_app


def prepare_header(headers):
    """
    Prepare header
    """
    if headers is None:
        headers = {}
    authorization = ''
    app = ''
    if request:
        authorization = request.headers['Authorization'] if 'Authorization' in request.headers.keys() else ''
        app = request.headers['App'] if 'App' in request.headers.keys() else ''
    return {**{'Authorization': authorization, 'App': app}, **headers}


def request_get(url, params=None, headers=None):
    """
    Add authentication when sending "get" requests
    """
    if params is None:
        params = {}
    return requests.get(url, params=params, headers=prepare_header(headers), verify=get_verify())


def request_post(url, data=None, headers=None):
    """
    Add authentication when sending "post" requests
    """
    if data is None:
        data = {}
    return requests.post(url, json=data, headers=prepare_header(headers), verify=get_verify())


def request_patch(url, data=None, headers=None):
    """
    Add authentication when sending "patch" requests
    """
    if data is None:
        data = {}
    return requests.patch(url, json=data, headers=prepare_header(headers), verify=get_verify())


def request_files(method, url, data=None, headers=None):
    """
    Add authentication when sending "post or patch" requests with files
    """
    if data is None:
        data = {}
    return requests.request(method, url, files=data, verify=get_verify(), headers=prepare_header(headers))


def dynamic_request(method, url, data=None, headers=None, form_data=False):
    """
    Method to do dynamic requests
    """
    if data is None:
        data = {}
    if form_data:
        return requests.request(method, url, files=data, verify=get_verify(), headers=prepare_header(headers))
    return requests.request(method, url, json=data, verify=get_verify(), headers=prepare_header(headers))


def get_verify():
    if 'REQUEST_VERIFY' in current_app.config.keys():
        return current_app.config['REQUEST_VERIFY']
    return False
