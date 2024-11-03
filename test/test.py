import json
import requests

with open('Credit_API.postman_collection.json') as f:
    collection = json.load(f)

for item in collection['item']:
    print("Item:", json.dumps(item, indent=2))

    if 'request' not in item:
        print(f"No request found for item: {item['name']}")
        continue

    request = item['request']
    request_name = item['name']
    
    method = request['method']
    url = request['url']['raw']
    headers = {h['key']: h['value'] for h in request.get('header', [])}
    body = request.get('body', {}).get('raw', None)

    print(f"Running {request_name}: {method} {url}")

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=body)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=body)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        print(f"Unsupported method: {method}")
        continue

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}\n")
