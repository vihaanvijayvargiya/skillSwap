import requests

url = "http://localhost:3000/api/appointments/my-appointments"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4MDIyNWJmZWIxNDYzMjFiNTRiNDJmNSIsImV4cCI6MTc0NzU2MzE5OX0.x81TAze4GZHMGI-tjIzuQSfbFQYC9KX-bGg-1NbeXzE"  # User token
}

# Test without filter
response = requests.get(url, headers=headers)
print("All appointments:")
print(response.status_code)
print(response.json())

# Test with status filter
url_with_filter = f"{url}?status=scheduled"
response = requests.get(url_with_filter, headers=headers)
print("\nOnly scheduled appointments:")
print(response.status_code)
print(response.json())