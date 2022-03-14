from kivy.network.urlrequest import UrlRequest
import urllib.parse
import json


def success(req, result):
    print('success')


def fail(req, result):
    print('fail')


def error(req, result):
    print('error')


def progress(req, result, chunk):
    print('loading')


def login_post(url: str, username: str, password: str):
    values = {'username': f'{username}', 'password': f'{password}'}
    # converted data to json type 
    params = urllib.parse.urlencode(values)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_body=params, req_headers=headers, verify=False)
    req.wait()
    print(req.result)
    return req.result
