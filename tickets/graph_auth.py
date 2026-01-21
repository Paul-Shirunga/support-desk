import requests
from django.conf import settings


def get_graph_token():
    url = f"https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/token"

    data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception(f"Token error: {response.text}")

    return response.json()["access_token"]
