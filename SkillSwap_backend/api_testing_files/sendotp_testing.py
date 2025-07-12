import requests

url = "http://localhost:3000/api/auth/send-otp"
params = {"mobile": "+917471141860"}

response = requests.post(url, params=params)
print(response.json())
