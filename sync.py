import requests
import json
import base64
from cred import username, api_token

domain = "telc.atlassian.net"
credentials = f"{username}:{api_token}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

def get_workspaceId():
    url = f"https://{domain}/rest/servicedeskapi/assets/workspace"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    data = response.json()
    return data.get('values')[0].get('workspaceId')



def get_objectIds():
    url = f"https://api.atlassian.com/jsm/assets/workspace/{workspace_id}/v1/object/aql"
    startAt = 0
    maxResults = 4

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }
    query = {
        'startAt': startAt,
        'maxResults': maxResults,
        'includeAttributes': 'false',
    }
    payload = json.dumps( {
        "qlQuery": 'objectType = "Managed Devices"'
    } )
    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    params=query
    )
    data = json.loads(response.text)
    return [obj['avatar']['objectId'] for obj in data.get('values', []) if any(attr.get('objectTypeAttributeId') == "285" for attr in obj.get('attributes', []))]



def fetch_userEmail(objectId):
    url = f"https://api.atlassian.com/jsm/assets/workspace/{workspace_id}/v1/object/{objectId}/attributes"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    data = json.loads(response.text)
    filtered_value = None
    for item in data:
        if item.get('objectTypeAttributeId') == '285':
            object_attribute_values = item.get('objectAttributeValues', [])
            if object_attribute_values:
                filtered_value = object_attribute_values[0].get('value')
            break

    # Ergebnis ausgeben
    if filtered_value:
        print(filtered_value)
    else:
        print("Kein Eintrag mit der id 285 gefunden.")



workspace_id = get_workspaceId()

object_type = "Managed Devices"
fetch_userEmail(456)