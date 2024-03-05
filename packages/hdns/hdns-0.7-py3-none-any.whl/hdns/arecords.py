import requests
import sys
import json

def get_all(zone_id, auth_api_token):
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records",
            params={
                "zone_id": zone_id,
            },
            headers={
                "Auth-API-Token": auth_api_token,
            },
        )

        response_json = response.json()
        records = response_json.get("records", [])
        type_a_records = []
        for record in records:
            if record.get("type") == "A":
                type_a_record = {key: value for key, value in record.items() if key not in ["created", "modified"]}
                type_a_records.append(type_a_record)

        return type_a_records
        
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed:', e)
        sys.exit(1)

def get_record(auth_api_token, record_id):
    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/records/" + record_id,
            headers={
                "Auth-API-Token": auth_api_token,
            },
        )
        response_json = response.json()
        return response_json["record"]
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def insert_records(auth_api_token, data_payload):

    try:
        response = requests.put(
            url="https://dns.hetzner.com/api/v1/records/bulk",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": auth_api_token,
            },
            data=json.dumps(
                {
                    "records": data_payload
                })
        )
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
