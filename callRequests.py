import requests
import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
# TEST
from flask import make_response

#app = Flask(__name__)
#CORS(app)

app = Flask(__name__)

origins = [
        "https://apostats.vercel.app",
        "http://localhost:3000"
        ]

cors = CORS(app, resources={r"/get_all_calls": {"origins": origins}})

_INITJULIA = 0
_INITMILLA = 0
_INITVALDEMAR = 0
_INITSOFIA = 0
_INITFABIAN = 0

UsersKundtjanst = {
    "JULIA": "0104102466",
    "MILLA": "0104104951",
    "VALDEMAR": "0104102495",
    "SOFIA": "0104102496",
    "FABIAN": "0104104956",
}

UsersAPI = {
        #"0104104956": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1MzY3OTU3IiwiYXVkIjoiKiIsImlzcyI6InR2eCIsImlhdCI6MTcwNDI3Mjk4OSwianRpIjoiMTQzMjEzNjIifQ.1y2DuYqnePo8vYMfOor7sfS9OhOidLOhUEJstW90_pFvVHR7PrCkVx5MT-W2-GVumuYFcdFyH4vtZA9yyGIAVg",
    "0104104956": os.environ['TELAVOX_API_KEY_FABIAN'],
    #"0104102466": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1MzE3NDUxIiwiYXVkIjoiKiIsImlzcyI6InR2eCIsImlhdCI6MTcwNDIwODYyNywianRpIjoiMTQyNzcwMjMifQ.gYRDeaaq93rLBjFnJL_t8_1gmztUwiYU7MYjxkFYVHuAdUjxov7Fl3fNw37XssjHhtlZezQSsGDSTk318Ykhwg",
    "0104102466": os.environ['TELAVOX_API_KEY_JULIA'],
    #"0104102496": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1MzE3NDg0IiwiYXVkIjoiKiIsImlzcyI6InR2eCIsImlhdCI6MTcwMzg0NTI1NSwianRpIjoiMTQwMjY2MDQifQ.Q_G41EqslClMFoAB1uaAuM67sjGtbHv944S32sY67ZcIsJD32ocDHabjsXK7uzTRjVCEFDaVDiwdSOppWN6zhQ",
    "0104102496": os.environ['TELAVOX_API_KEY_SOFIA'],    
    #"0104102495": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1MzE3NDgxIiwiYXVkIjoiKiIsImlzcyI6InR2eCIsImlhdCI6MTcwMzg1MjE5OCwianRpIjoiMTQwMzEzODQifQ.rNpMePUxpdGV6umE7KzNudSrgL5WnCoVF8B2s228VxHZGdOU6tR4WCn602LQkT_grhTGdW7dq_vv3BwrEesW9A",
    "0104102495": os.environ['TELAVOX_API_KEY_VALDEMAR'],    

    "0104104951": os.environ['TELAVOX_API_KEY_MILLA'],
}

previous_calls = {
    "JULIA": None,
    "MILLA": None,
    "VALDEMAR": None,
    "SOFIA": None,
    "FABIAN": None,
}

all_calls = {
    "JULIA": _INITJULIA,
    "MILLA": _INITMILLA,
    "VALDEMAR": _INITVALDEMAR,
    "SOFIA": _INITSOFIA,
    "FABIAN": _INITFABIAN,
}

def getCurrentDate():
    current_date = datetime.now()
    todayDate = current_date.strftime('%Y-%m-%d')
    return todayDate

today_date = getCurrentDate()

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
            
    if today_date != getCurrentDate():
        today_date = getCurrentDate()
        for username in all_calls:
            all_calls[username] = 0
        
    return all_calls

@app.route('/get_all_calls', methods=['GET'])
def get_all_calls():
    all_user_calls = countCallsForAllUsers()
    # TEST
    response = make_response(jsonify(all_user_calls))
    # TEST
    response.headers['Access-Control-Allow-Origin'] = 'https://apo-ex-call-stats.vercel.app'
    return jsonify(all_user_calls)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
