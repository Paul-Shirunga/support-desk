import requests
from django.conf import settings
from .graph_auth import get_graph_token


def get_latest_email():
    token = get_graph_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = (
        f"https://graph.microsoft.com/v1.0/users/"
        f"{settings.MAILBOX_USER}/mailFolders/Inbox/messages"
        "?$top=1&$orderby=receivedDateTime desc"
    )

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    messages = data.get("value", [])

    if not messages:
        return None

    msg = messages[0]

    return {
        "id": msg["id"],
        "subject": msg.get("subject"),
        "from": msg["from"]["emailAddress"]["address"],
        "body": msg["body"]["content"]
    }
