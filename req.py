import requests

url = "http://localhost/api/v1/ancien_etudiants/upload_photo/"
files = {"uploaded_file": open("image.jpg", 'rb')}
res = requests.post(url=url, files=files)
print(res.text)
