import json
import requests


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


def get_find_by_district_data(dist_id, date):
    query_params = {"district_id": str(dist_id), "date": date}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 "
                      "Safari/537.36"}
    now_request = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",
                               params=query_params, headers=headers)
    now_response = now_request.json()
    return now_response


districts = {141: 'Central Delhi', 145: 'East Delhi', 140: 'New Delhi', 146: 'North Delhi', 147: 'North East Delhi',
             143: 'North West Delhi', 148: 'Shahdara', 149: 'South Delhi', 144: 'South East Delhi',
             150: 'South West Delhi', 142: 'West Delhi'}


def api_performance_testing(dist_id, date):
    calendar_data = get_current_data(dist_id)
    find_by_data = get_find_by_district_data(dist_id, date)
    find_by_path = f'find_by_{dist_id}_{date}.json'
    calendar_path = f'calendar_{dist_id}.json'
    with open(find_by_path, 'w') as file:
        json.dump(find_by_data, file)  # old_data.json.write(current_response)

    with open(calendar_path, 'w') as file:
        json.dump(calendar_data, file)  # old_data.json.write(current_response)


api_performance_testing(650, '08-06-2021')
