import requests
from datetime import datetime, timedelta

# Get tomorrow's date for testing
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Replace with an actual doctor ID from your database
doctor_id = "68723a9751917566d034f5d6"  

url = f"http://localhost:3000/api/appointments/{doctor_id}/available-slots?date={tomorrow}"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzIzOWRmZThhMGZkN2Y5Njc1NWI2NiIsImV4cCI6MTc1NDkwODM4M30.38DE1HYXi06irwd3-hXy7-KNQ-4xoPrRex6FSWrO1QM"  # User token
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())