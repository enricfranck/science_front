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

def get_mention_uuid(url:str,uuid_mention:str, token:str):
    values = {'uuid':f'{uuid_mention}'} 
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

def get_mention(url:str,token:str):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress, 
    req_headers=headers, verify=False, method='GET') 
    req.wait() 
    print(req.result)
    return req.result

def get_annee_univ(url:str,token:str):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress, 
    req_headers=headers, verify=False, method='GET') 
    req.wait()
    return req.result

def get_parcours_by_mention(url:str,uuid_mention:str, token:str):
    values = {'uuid_mention':f'{uuid_mention}'} 
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