import requests
import json

payload = {
        "operation":"sql",
        "sql":"update sync.operation set operations =\"{hello}\" where email = 'jaik@gmail.com'"
    }


url = "https://qcalls-damnik.harperdbcloud.com"

payload = json.dumps(payload)
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic ZGFtbmlrOmRhbW5paw==",
    'Cache-Control': "no-cache",
    'Postman-Token': "e774a008-e04f-4779-b828-18201a61c916"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.json())
print(response.json()[0])