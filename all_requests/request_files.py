import urllib

from kivy.network.urlrequest import UrlRequest


def success(req, result):
    print('success')


def fail(req, result):
    print('fail')


def error(req, result):
    print('error')


def progress(req, result, chunk):
    print('loading')


def download_file(url: str, annee: str, uuid_mention: str, token: str, path: str):
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', 'uuid_mention': f'{uuid_mention}'}
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, file_path=path, verify=False, method="GET")
    req.wait()
    return req.result
