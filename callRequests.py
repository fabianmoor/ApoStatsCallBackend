import requests
import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

#app = Flask(__name__)
#CORS(app)

app = Flask(__name__)
cors = CORS(app, resources={r"/get_all_calls": {"origins": "https://apo-ex-call-stats.vercel.app"}})


UsersKundtjanst = {
    "JULIA": "0104102466",
    "MILLA": "0104104951",
    "VALDEMAR": "0104102495",
    "SOFIA": "0104102496",
    "FABIAN": "0104104956"
}

UsersAPI = {
    "0104104956": os.environ['TELAVOX_API_KEY']
}

def getCurrentDate():
    current_date = datetime.now()
    todayDate = current_date.strftime('%Y-%m-%d')
    return todayDate

def countCallsForAllUsers():
    all_calls = {}
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
            calls_count = len(incoming_calls)
            all_calls[username] = calls_count
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception occurred for {username}: {req_err}")
            all_calls[username] = 0

    return all_calls

@app.route('/get_all_calls', methods=['GET'])
def get_all_calls():
    all_user_calls = countCallsForAllUsers()
    return jsonify(all_user_calls)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
