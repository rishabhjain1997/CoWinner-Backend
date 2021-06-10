import requests
import json
from dateutil import tz
from datetime import datetime, timedelta


class DayData:
    def __init__(self, day_value, district_id):
        self.date = self.get_current_date(day_value)
        self.json_file_name = f'find_by_json_{district_id}_{self.get_current_date(day_value)}.json'
        self.district_id = district_id
        self.data = self.get_current_data()
        self.new_sessions = self.calculate_session_updates()

    def get_current_data(self):
        # Returns Current data in JSON
        indian_date = self.date  # fetch today's date
        query_params = {"district_id": str(self.district_id),
                        "date": indian_date}  # dynamically pass district id cur batchdate
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 "
                          "Safari/537.36"}

        now_request = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",
                                   params=query_params, headers=headers)  # API Call

        now_response = now_request.json()  # dictionary of contents for batchdate
        return now_response

    @staticmethod
    def get_current_date(day_delta=0):
        """Function to fetch Indian format of the date of the current day in which job is running(IST timezone)"""
        india_tz = tz.gettz("Asia/Kolkata")
        now = datetime.now(tz=india_tz)
        today = str(now.date() + timedelta(days=day_delta))

        year, month, day = today.split('-')
        t1 = (day, month, year)
        indian_date = "-".join(t1)
        return indian_date

    @staticmethod
    def appointment_with_no_slots(session_data):
        return False if session_data['available_capacity'] > 0 else True

    @staticmethod
    def is_appointment_under_45(session_data):
        return False if session_data['min_age_limit'] == 45 else True

    def calculate_session_updates(self):
        """
        # Captures session details and updates if any new session is added

        # Parameters:
        #    dist_id (int): District ID

        # Returns:
        #    new_sessions(list): List having (session_id, center_id) for all new sessions

        """

        # Added dist_id parameter to old_response.json
        now_response = self.data
        prev_filepath = f'data/{self.json_file_name}'

        # read file old_data.json
        try:
            with open(prev_filepath, "r") as file:
                prev_response = json.loads(file.read())
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            with open(prev_filepath, 'w') as file:
                json.dump(now_response, file)  # old_data.json.write(current_response)
                return []

                # since we have stored the prev run's data in old_response, now the current run's data should be written
                # to old json

        with open(prev_filepath, 'w') as file:
            json.dump(now_response, file)  # old_data.json.write(current_response)

        sessions_prev = prev_response['sessions']
        sessions_now = now_response['sessions']

        now_dict = {}
        prev_dict = {}

        # generating {session id:session index} mappings for current run and prev run data
        for session_index in range(0, len(sessions_now)):
            now_dict.update({sessions_now[session_index]["session_id"]: session_index})

        for session_index in range(0, len(sessions_prev)):
            prev_dict.update({sessions_prev[session_index]["session_id"]: session_index})

        # filtering sessions which are unique to the current run
        new_sessions_update = {k: now_dict[k] for k in set(now_dict) - set(prev_dict)}

        updated_session_indices = list(new_sessions_update.values())
        return updated_session_indices

    def create_session_message(self):
        """
        # Returns message per unique session_data

        # Parameters:
        # (center_id, session_id, now_response) : center_id, session_id and JSON data

        # Returns:
        #   message (string): Message


        """
        now_response = self.data
        session_indices = self.new_sessions
        sessions = now_response['sessions']
        messages = []

        for index in session_indices:
            center = sessions[index]
            if self.appointment_with_no_slots(center) or not self.is_appointment_under_45(center):
                continue
            session_date = datetime.strptime(center['date'], '%d-%m-%Y').strftime('%d %B')
            age_category = '45 plus ages' if center['min_age_limit'] == 45 else '18-45 ages'
            fee = "Free" if center['fee'] == "0" else center['fee']
            # print(session_data['min_age_limit'])
            message = "\U0001F4CD" + f" Pincode *{center['pincode']}*\n" + \
                      "\U0001F3E5" + f" {center['name'].upper()}\n" + \
                      "\U0001F5D3" + f" {session_date}\n" + \
                      "\U0001F489" + f" {center['vaccine']}\n" + \
                      "\U0001F4B0" + f" {fee}\n" + \
                      "\U0001F382" + f" {age_category}\n" + \
                      "\U000025B6" + f" Dose 1: {center['available_capacity_dose1']} slots\n" + \
                      "\U000023E9" + f" Dose 2: {center['available_capacity_dose2']} slots\n" + \
                      "CoWin: selfregistration.cowin.gov.in\n" + \
                      "-----------" + \
                      "-----------" + \
                      "-----------" + \
                      "-----------\n"
            messages.append(message)
        return messages
