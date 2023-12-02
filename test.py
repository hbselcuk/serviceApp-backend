import requests

import json

# Define the base URL for your FastAPI server
base_url = "http://localhost:8000"  # Update with your actual FastAPI server URL

# Define the data you want to send in the POST request
data = {
    "param_0": "getstuff",
    "param_1": 10,
    "param_2": 0
}

data = json.dumps(data)

token = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJkNGQ5YzRmOS0yMzBmLTRjZjYtOGRmNS05NDA2N2Y1OTA1MmMifQ.eyJleHAiOjE3MDg3NjUyOTMsImlhdCI6MTcwMDEyNTI5MywianRpIjoiMTFjYjRkYWYtMzI5MS00MTU0LWFkMGYtMTI2YjU2OWM2NWE5IiwiaXNzIjoiaHR0cHM6Ly82Mi4xNzEuMTkwLjIzNDo1MDAwL2F1dGgvcmVhbG1zL21vdl9zZXJ2aWNlX2FwcCIsImF1ZCI6Imh0dHBzOi8vNjIuMTcxLjE5MC4yMzQ6NTAwMC9hdXRoL3JlYWxtcy9tb3Zfc2VydmljZV9hcHAiLCJ0eXAiOiJJbml0aWFsQWNjZXNzVG9rZW4ifQ.r7tcDLOEFh0TUf_nNydo_UKBmesdPNnecK3Cxw4GwHo"}

# Make the POST request to the /restAPI/getStuff/ route
response = requests.post(f"{base_url}/restAPI/getStuff/", json=data, headers=token)

#response = requests.get(f"{base_url}/api/private", headers=token)

# Print the response from the server
print(response.status_code)
print(response.content)