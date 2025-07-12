import requests

url = "http://localhost:3000/api/doctors/slot-duration"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4MDIyNjg5MzcxNjU4Yjc2Mzk0MTJmNyIsImV4cCI6MTc0NzU2MzQwMX0.mTCpzMdud9NqOjVWeBikQH25Ro5EeW4fY8Y8A2Tz9KE",
    "Content-Type": "application/json"
}
data = 15  # 15 minutes per slot

response = requests.put(url, headers=headers, json=data)
print(response.status_code)
print(response.json())