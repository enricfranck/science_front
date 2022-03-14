from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
import urllib.parse
import json


# def success(req, result):
#     print('success')
# def fail(req, result):
#     print('fail')
# def error(req, result):
#     print('error')
# def progress(req, result, chunk):
#      print('loading')
# values = {'username':'admin@science.com', 'password':'aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5'}
# # converted data to json type
# params = urllib.parse.urlencode(values)
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# req = UrlRequest(f"http://localhost/api/v1/login/access-token", on_success=success, on_failure=fail, on_error=error, on_progress=progress,
# req_body=params, req_headers=headers)
# req.wait()
# print(req.result)

def create_list_tuple(list_data: list):
    response = []
    for index, data in enumerate(list_data):
        if index == 0:
            response.append((f"{data}", dp(10)))
        else:
            response.append((f"{data}", dp(20)))
    return response

if __name__ == "__main__":
    data = ["Num Ce", "anglais", "francais"]
    create_list_tuple(data)