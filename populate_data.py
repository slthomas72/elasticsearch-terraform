import json
import requests
from faker import Faker

fake = Faker()

# Generate fake data and format it as ndjson
actions = ""
for _ in range(1000):
    action = {"index": {}}
    doc = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'created_at': fake.date_time_this_decade().isoformat()
    }
    actions += json.dumps(action) + "\n" + json.dumps(doc) + "\n"

# Send bulk request to Elasticsearch
url = 'http://localhost:9200/people/_bulk'
headers = {'Content-Type': 'application/x-ndjson'}
response = requests.post(url, headers=headers, data=actions, auth=('', ''))  # Replace with your actual username and password but hide later get from terraform global vals

# Check the response
if response.status_code == 200:
    print("Data indexed successfully.")
else:
    print(f"Failed to index data. Status code: {response.status_code}")
    print(response.text)