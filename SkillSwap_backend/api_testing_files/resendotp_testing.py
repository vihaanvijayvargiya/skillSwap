import requests

url = "http://localhost:3000/api/auth/resend-otp"
params = {"mobile": "+917470731545"}

response = requests.post(url, params=params)
print(response.json())
