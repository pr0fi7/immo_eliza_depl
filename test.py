import requests
import json

with open("test.json", "r") as f:
    data = json.load(f)

response = requests.post("http://127.0.0.1:8000/predict", json=data["data"])

print("Response Status Code:", response.status_code)

if response.status_code == 200:
    print("Response Content:")
    print(response.json())
else:
    print("Error:", response.text)



