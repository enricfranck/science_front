from typing import Any, List, Dict

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


def trasnform_list(data: list) -> List[Dict[Any, Any]]:
    """
    This methode transforme a list of list to a dick, and the first row is a key and the other is a value
    :param data: list of list
    :return: dict of the element in the list
    """
    all_data = []
    for index, item in enumerate(data):
        if index != 0:
            all_data.append(dict(zip(data[0], item)))
    return all_data


def create_json(list_key: list, list_value: list):
    data = list_key + list_value



def get_mention_uuid(url: str, uuid_mention: str, token: str):
    values = {'uuid': f'{uuid_mention}'}
    # converted data to json type 
    params = urllib.parse.urlencode(values)
    url = f"{url}?{params}"
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    return req.result


def get_mention(url: str, token: str):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    print(req.result)
    return req.result


def get_annee_univ(url: str, token: str):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    return req.result


def get_parcours_by_mention(url: str, uuid_mention: str, token: str):
    values = {'uuid_mention': f'{uuid_mention}'}
    # converted data to json type
    params = urllib.parse.urlencode(values)
    url = f"{url}?{params}"
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    return req.result


def create_mention(url: str, token: str, payload: str):
    """
    To create the MENTION
    :param url:
    :param token:
    :param payload:
    :return:
    """
    return create_connection(url, {}, payload, token, "POST")


def create_connection(url: str, values: dict, payload: Any, token: str, methode: str):
    """
    call this function to access the url
    :param url: api url
    :param values: list of parameters
    :param payload: the request body
    :param token: the token result of the login
    :param methode: the methode "POST, GET, PUT or DELETE "
    :return:
    """
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    if len(values) != 0:
        url = f"{url}?{params}"
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, req_body=payload, verify=False, method=methode, timeout=15)
    req.wait()
    return req.result
