def create_user_list(path):
    import firebase_admin
    from firebase_admin import db
    from firebase_admin import credentials
    cred = credentials.Certificate("cowinner-20464-firebase-adminsdk-ftwj6-deb6dfd475.json")
    firebase_admin.initialize_app(cred,
                                  {
                                      'databaseURL': 'https://cowinner-20464-default-rtdb.asia-southeast1.firebasedatabase.app/'
                                  })
    ref = db.reference(path)

    return list(map(lambda phone_number: phone_number.lstrip('+'), ref.get().keys()))


def send_notifications(user_list, message):
    import wati_auth
    import requests
    headers = {
        'accept': '*/*',
        'Authorization': wati_auth.access_token,
        'Content-Type': 'application/json-patch+json',
    }

    responses = []
    for user in user_list:
        send_message_endpoint = wati_auth.base_url + '/api/v1/sendSessionMessage/' + str(user)
        response = requests.post(send_message_endpoint + '?messageText=' + message, headers=headers)
        responses.append({user: response.json()})
    return responses
