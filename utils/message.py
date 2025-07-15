import requests


def send_initial_message(recipient_id, phone_number_id, access_token):
    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": str(recipient_id),
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def send_message(recipient_id, phone_number_id, access_token, message):
    try:
        url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": str(recipient_id),
            "type": "text",
            "text": {
                "body": message
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: \n\n\n{e}\n\n\n")
        return None