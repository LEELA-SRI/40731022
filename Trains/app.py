from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/trains', methods=['GET'])
def get_trains():

    url = 'http://104.211.219.98/train/auth'
    credentials = {
    "companyName": "Train Central",
    "clientID": "94edbb0a-ecc7-4e0d-a77e-edd4d786429b",
    "clientSecret": "lwiuIbjJbgkIxMkI",
    "ownerName": "leela",
    "ownerEmail": "leelasric@gmail.com",
    "rollNo": "40731022"
    }
    post_req = requests.post(url, json=credentials)
    post_req_response =post_req.json()
    token =post_req_response["access_token"]

    get_trains = requests.get("http://104.211.219.98:80/train/trains",headers={
        'Authorization': f'Bearer {token}'
    })

    trains_data = get_trains.json()
    return 'hi'


if __name__ == '__main__':
    app.run(debug=True,port=3000)