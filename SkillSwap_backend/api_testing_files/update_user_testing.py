import requests

url = "http://localhost:3000/api/users/update-profile"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzIzYTk3NTE5MTc1NjZkMDM0ZjVkNiIsImV4cCI6MTc1NDkwODU2N30.AvWXzDjFrOiV-gBDIj9JlnLAlbCSGSUAu-AXVSPQqSg",
    "Content-Type": "application/json"
}
data = {  
    "weight": 42,
    "height": 142,
    "name":"Sakshi Raut",
    "skills_offered": ["Flutter", "Gen AI"],
    "skills_wanted": ["Data Science"]
}


response = requests.put(url, headers=headers, json=data)
print(response.status_code)
print(response.json())