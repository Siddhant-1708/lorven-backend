import requests

url = "http://127.0.0.1:8000/upload-voice/"
files = {'file': open("Recording.wav", 'rb')}  # Make sure this matches the downloaded file name

response = requests.post(url, files=files)
print(response.status_code)
print(response.json())
