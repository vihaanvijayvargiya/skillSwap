import requests

url = "http://localhost:3000/api/users/me"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzFlOTYwZWE4MjE0OWI1ZmY1ZWNmZCIsImV4cCI6MTc1NDg4Nzc3Nn0.WqTr6WaOxX7x4mvcIpeTnpVYoqVKMMghr-KpoqB-7w8"
}

response = requests.get(url, headers=headers)
print(response.json())
