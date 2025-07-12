import requests
from datetime import datetime, timedelta

# Get tomorrow's date for testing
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

url = "http://localhost:3000/api/appointments/book-appointment"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NzIzOWRmZThhMGZkN2Y5Njc1NWI2NiIsImV4cCI6MTc1NDkwODM4M30.38DE1HYXi06irwd3-hXy7-KNQ-4xoPrRex6FSWrO1QM",  # User token
    "Content-Type": "application/json"
}
data = {
    "user2_id": "68723a9751917566d034f5d6",  # Replace with actual user2 ID
    "appointment_date": tomorrow,
    "appointment_time": "13:45",  # Ensure this time is in the user2's availability
    "reason": "i am passionate to learn flutter and i want to learn it from you",
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())

# Save the appointment ID for other tests
if response.status_code == 201:
    appointment_id = response.json().get("appointment_id")
    print(f"Created appointment ID: {appointment_id}")
    
    # Save to a file for other tests to use
    # with open("test_appointment_id.txt", "w") as f:
    #     f.write(appointment_id)