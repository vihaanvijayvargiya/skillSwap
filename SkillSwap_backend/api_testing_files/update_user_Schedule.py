import requests

url = "http://localhost:3000/api/users/update-schedule"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzIzYTk3NTE5MTc1NjZkMDM0ZjVkNiIsImV4cCI6MTc1NDkwODU2N30.AvWXzDjFrOiV-gBDIj9JlnLAlbCSGSUAu-AXVSPQqSg",
    "Content-Type": "application/json"
}
data = {
    "monday": ["09:00-12:00", "15:00-18:00"],
    "tuesday": ["09:00-12:00"],
    "wednesday": [],
    "thursday": ["10:00-14:00"],
    "friday": ["09:00-12:00", "13:00-15:00"],
    "saturday": ["10:00-13:00"],
    "sunday": ["13:00-15:00"]
}

response = requests.put(url, headers=headers, json=data)
print(response.status_code)
print(response.json())