import requests
import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask import make_response
import json


app = Flask(__name__)

origins = [
        "https://apostats.vercel.app",
        "http://localhost:3000"
        ]

cors = CORS(app, resources={
    r"/get_all_calls": {"origins": origins},
    r"/get_fabian": {"origins": origins},
    r"/change_date": {"origins": origins},
    })

all_calls = {
    "JULIA": 4-1,
    "MILLA": 6-1,
    "VALDEMAR": 6-1,
    "SOFIA": 2-1,
    "FABIAN": 5-1,
}

UsersKundtjanst = {
    "JULIA": "0104102466",
    "MILLA": "0104104951",
    "VALDEMAR": "0104102495",
    "SOFIA": "0104102496",
    "FABIAN": "0104104956",
}

UsersAPI = {
    "0104104956": os.environ['TELAVOX_API_KEY_FABIAN'],
    "0104102466": os.environ['TELAVOX_API_KEY_JULIA'],
    "0104102496": os.environ['TELAVOX_API_KEY_SOFIA'],    
    "0104102495": os.environ['TELAVOX_API_KEY_VALDEMAR'],    
    "0104104951": os.environ['TELAVOX_API_KEY_MILLA'],
}
    
def clear_calls():
    global all_calls
    for i in all_calls:
        all_calls[i] = 0

def getCurrentDate():
    current_date = datetime.now()
    todayDate = current_date.strftime('%Y-%m-%d')
    return todayDate


def countCallsForAllUsers():
    global today_date, all_calls, previous_calls
    for username, user_id in UsersKundtjanst.items():
        USER_API = UsersAPI.get(user_id)
        headers = {
            "Authorization": f"Bearer {USER_API}",
        }
        params = {
            "fromDate": getCurrentDate(),
            "toDate": getCurrentDate(),
        }
        try:
            response = requests.get("https://api.telavox.se/calls", headers=headers, params=params)
            response.raise_for_status()
            incoming_calls = response.json().get('incoming', [])

            if incoming_calls:
                latest_call_id = incoming_calls[0]['callId']
                if previous_calls[username] != latest_call_id:
                    all_calls[username] += 1
                    print(f"{username} took a call. Added one call.")
                    previous_calls[username] = latest_call_id
            
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception occurred for {username}: {req_err}")
        
    return all_calls

def is_sum_greater(data):
    return sum(data.values())



# Setting previous_calls & today_date
previous_calls = {user: None for user in all_calls}
today_date = getCurrentDate()


# app.routes
@app.route('/get_fabian', methods=['GET'])
def get_fabian():
    global all_calls
    all_calls['FABIAN'] += 1
    return "Finish"

@app.route('/change_date', methods=['GET'])
def change_date():
    global today_date
    today_date = "2024-01-10"
    return "Date Changed"

@app.route('/get_all_calls', methods=['GET'])
def get_all_calls():
    global today_date
    print(today_date)
    print(getCurrentDate())
    if today_date != getCurrentDate():
        today_date = getCurrentDate()
        for username in all_calls:
            all_calls[username] = 0
            
    all_user_calls = countCallsForAllUsers()
    
    try:
        if is_sum_greater(all_user_calls) > is_sum_greater(previous_sum):
            return all_user_calls
        elif is_sum_greater(all_user_calls) < is_sum_greater(previous_sum):
            print("Woops, the json got fucked, but was luckily saved by the exception.")
            return previous_sum
    except NameError:
        previous_sum = all_user_calls
        return all_user_calls

if __name__ == '__main__':
    app.run(debug=True)
