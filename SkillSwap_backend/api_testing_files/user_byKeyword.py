import requests

# Correct URL with query parameter
url = "http://localhost:3000/api/users/search"  # Note this should be "doctors" not "users"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzIzOWRmZThhMGZkN2Y5Njc1NWI2NiIsImV4cCI6MTc1NDkwODM4M30.38DE1HYXi06irwd3-hXy7-KNQ-4xoPrRex6FSWrO1QM"
}

# Send keyword as a query parameter, not a header
params = {
    "keyword": "Flutter"  # Example keyword to search for
}

response = requests.get(url, headers=headers, params=params)
print(response.json())