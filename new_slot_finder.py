import requests
import json
from dateutil import tz
from datetime import datetime

def getcurdate():
"""Function to fetch Indian format of the date of the current day in which job is running(IST timezone)"""
    India_tz = tz.gettz("Asia/Kolkata")
    now = datetime.now(tz=India_tz)
    todayy = str(now.date())
    year,month,day = todayy.split('-')
    t1 = (day,month,year)
    indian_date = "-".join(t1)
    return indian_date

def district_wise_updates(dist_id):
    indian_date = getcurdate()      #fetch today's date
    query_params={"district_id":str(dist_id),"date": indian_date} # dynamically pass district id cur batchdate 
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    now_request = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",params=query_params,headers=headers)#API Call

    #TODO: Need to include relative filepaths
    prev_filepath = "C:\\Users\\Tanmaya\\Documents\\old_response.json"
    update_filepath = "C:\\Users\\Tanmaya\\Documents\\update_response.json"

    now_response = now_request.json()   #dictionary of contents for batchdate

    #read file old_data.json
    with open(prev_filepath, "r") as file:
        prev_response = json.loads(file.read())      
        
    #since we have stored the prev run's data in old_response, now the current run's data should be written to old json
    with open(prev_filepath,'w') as file:
            json.dump(now_response, file)	                 #old_data.json.write(current_response)

    centers_prev = prev_response['centers']
    centers_now = now_response['centers']

    now_dict={}
    prev_dict={}

    #generating {session id:center id} mappings for current run and prev run data
    
    for center_index in range(0,len(centers_now)):
        percenter_session=dict(map(lambda x: (x["session_id"],centers_now[center_index]['center_id']), centers_now[center_index]["sessions"]))
        now_dict.update(percenter_session)

    for center_index in range(0,len(centers_prev)):
        percenter_session=dict(map(lambda x: (x["session_id"],centers_prev[center_index]['center_id']), centers_prev[center_index]["sessions"]))
        prev_dict.update(percenter_session)

    #filtering sessions which are unique to the current run only 
    unique_values = { k : now_dict[k] for k in set(now_dict) - set(prev_dict) }
            
    print("The newly updated centers are", unique_values)



