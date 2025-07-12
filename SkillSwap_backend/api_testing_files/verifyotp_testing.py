import requests

url = "http://localhost:3000/api/auth/verify-otp"
params = {
    "mobile": "+917471141860",
    "otp": "844387"  # Replace with actual OTP
}

response = requests.post(url, params=params)
print(response.json())
