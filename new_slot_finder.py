import requests
import json

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
now_request = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=621&date=30-05-2021",headers=headers)
prev_filepath = "C:\\Users\\Tanmaya\\Documents\\old_response.json"
update_filepath = "C:\\Users\\Tanmaya\\Documents\\update_response.json"
now_response = now_request.json()
 
with open(prev_filepath, "r") as file:
    prev_response = json.loads(file.read())      #read file old_data.json
    
with open(prev_filepath,'w') as file:
	json.dump(now_response, file)	        #since we have stored the prev run's data in old_response, now the current run's data should be written to old json
                                                #old_data.json.write(current_response)

centers_prev = prev_response['centers']
centers_now = now_response['centers']

"""nowcenter_ids = set() 
prevcenter_ids = set()

for i in range (len(centers_prev)):
    prevcenter_ids.add(centers[i]["center_id"])

for i in range (len(centers_now)):
    nowcenter_ids.add(centers[i]["center_id"])

new_centers= nowcenter_ids-prevcenter_ids"""

#print("the centers which have been added newly are" , new_centers)

#new_centers1 = nowcenter_ids.intersection(prevcenter_ids)

now_dict={}
prev_dict={}

for i in range(0,len(centers_now)):
    percenter_session=dict(map(lambda x: (x["session_id"],centers_now[i]['center_id']), centers_now[i]["sessions"]))
    now_dict.update(percenter_session)

for i in range(0,len(centers_prev)):
    percenter_session=dict(map(lambda x: (x["session_id"],centers_prev[i]['center_id']), centers_prev[i]["sessions"]))
    prev_dict.update(percenter_session)

value = { k : now_dict[k] for k in set(now_dict) - set(prev_dict) }
	
print("The newly updated centers are", value.items())



