
response = requests.put(url, headers=headers, json=data)
print(response.status_code)
print(response.json())