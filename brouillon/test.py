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
values = {'username':'admin@science.com', 'password':'aze135azq35sfsnf6353sfh3xb68yyp31gf68k5sf6h3s5d68jd5'} 
# converted data to json type 
params = urllib.parse.urlencode(values)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
req = UrlRequest(f"http://localhost/api/v1/login/access-token", on_success=success, on_failure=fail, on_error=error, on_progress=progress, 
req_body=params, req_headers=headers) 
req.wait() 
print(req.result)