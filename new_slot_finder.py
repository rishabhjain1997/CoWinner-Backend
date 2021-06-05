import requests
import json
from dateutil import tz
from datetime import datetime


def get_current_date():
    """Function to fetch Indian format of the date of the current day in which job is running(IST timezone)"""
    india_tz = tz.gettz("Asia/Kolkata")
    now = datetime.now(tz=india_tz)
    today = str(now.date())
    year, month, day = today.split('-')
    t1 = (day, month, year)
    indian_date = "-".join(t1)
    return indian_date


def is_appointment_under_45(session_data):
    return False if session_data['min_age_limit'] == 45 else True


def get_current_data(dist_id):
    # Returns Current data in JSON
    indian_date = get_current_date()  # fetch today's date
    query_params = {"district_id": str(dist_id), "date": indian_date}  # dynamically pass district id cur batchdate
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 "
                      "Safari/537.36"}
    now_request = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
                               params=query_params, headers=headers)  # API Call
    now_response = now_request.json()  # dictionary of contents for batchdate
    return now_response


def calculate_session_updates(dist_id, now_response):
    """
    # Captures session details and updates if any new session is added

    # Parameters:
    #    dist_id (int): District ID

    # Returns:
    #    new_sessions(list): List having (session_id, center_id) for all new sessions   

    """

    # Added dist_id parameter to old_response.json
    prev_filepath = f"old_response_{dist_id}.json"

    # read file old_data.json
    try:
        with open(prev_filepath, "r") as file:
            prev_response = json.loads(file.read())
    except FileNotFoundError as e:
        with open(prev_filepath, 'w') as file:
            json.dump(now_response, file)  # old_data.json.write(current_response)
            return []

            # since we have stored the prev run's data in old_response, now the current run's data should be written
            # to old json

    with open(prev_filepath, 'w') as file:
        json.dump(now_response, file)  # old_data.json.write(current_response)

    centers_prev = prev_response['centers']
    centers_now = now_response['centers']

    now_dict = {}
    prev_dict = {}

    # generating {session id:center id} mappings for current run and prev run data

    for center_index in range(0, len(centers_now)):
        sessions = dict(map(lambda x: (x["session_id"], centers_now[center_index]['center_id']),
                            centers_now[center_index]["sessions"]))
        now_dict.update(sessions)

    for center_index in range(0, len(centers_prev)):
        sessions = dict(map(lambda x: (x["session_id"], centers_prev[center_index]['center_id']),
                            centers_prev[center_index]["sessions"]))
        prev_dict.update(sessions)

    # filtering sessions which are unique to the current run
    new_sessions = list({k: now_dict[k] for k in set(now_dict) - set(prev_dict)}.items())
    return new_sessions


def appointment_with_no_slots(session_data):
    return False if session_data['available_capacity'] > 0 else True


def create_session_message(center_id, session_id, now_response):
    """
    # Returns message per unique session_data

    # Parameters:
    # (center_id, session_id, now_response) : center_id, session_id and JSON data

    # Returns:
    #   message (string): Message  
    

    """
    centers = now_response['centers']
    center_data = list(filter(lambda center: center['center_id'] == int(center_id), centers))[0]
    session_data = list(filter(lambda session: session['session_id'] == session_id, center_data['sessions']))[0]

    # Add filters here
    if not is_appointment_under_45(session_data) or appointment_with_no_slots(session_data):
        return None

    session_date = datetime.strptime(session_data['date'], '%d-%m-%Y').strftime('%d %B')
    age_category = '45 plus ages' if session_data['min_age_limit'] == 45 else '18-45 ages'
    # print(session_data['min_age_limit'])
    message = "\U0001F4CD" + f" Pincode *{center_data['pincode']}*\n" + \
              "\U0001F3E5" + f" {center_data['name'].upper()}\n" + \
              "\U0001F5D3" + f" {session_date}\n" + \
              "\U0001F489" + f" {session_data['vaccine']}\n" + \
              "\U0001F4B0" + f" {center_data['fee_type']}\n" + \
              "\U0001F382" + f" {age_category}\n" + \
              "\U000025B6" + f" Dose 1: {session_data['available_capacity_dose1']} slots\n" + \
              "\U000023E9" + f" Dose 2: {session_data['available_capacity_dose2']} slots\n" + \
              "CoWin: selfregistration.cowin.gov.in\n" + \
              "-----------" + \
              "-----------" + \
              "-----------" + \
              "-----------\n"
    return message
