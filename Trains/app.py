from flask import Flask,request,jsonify,render_template
import requests
import datetime

app = Flask(__name__)

url = 'http://104.211.219.98/train/auth'
credentials = {
    "companyName": "Train Central",
    "clientID": "94edbb0a-ecc7-4e0d-a77e-edd4d786429b",
    "clientSecret": "lwiuIbjJbgkIxMkI",
    "ownerName": "leela",
    "ownerEmail": "leelasric@gmail.com",
    "rollNo": "40731022"
    }

def sort_key(train):
    current_time = datetime.datetime.now()
    departure_time = datetime.datetime(
        year=current_time.year,
        month=current_time.month,
        day=current_time.day,
        hour=train["departureTime"]["Hours"],
        minute=train["departureTime"]["Minutes"],
        second=train["departureTime"]["Seconds"],
    )
    if departure_time <= current_time + datetime.timedelta(minutes=30):
        return float("inf")
    return (
        train["trainNumber"],
        -train["seatsAvailable"]["sleeper"],
        -train["seatsAvailable"]["AC"],
        -train["departureTime"]["Hours"],
        -train["departureTime"]["Minutes"],
        -train["departureTime"]["Seconds"],
        train["delayedBy"]
    )  


@app.route('/trains', methods=['GET'])
def get_trains():

    
    post_req = requests.post(url, json=credentials)
    post_req_response =post_req.json()
    token =post_req_response["access_token"]

    get_trains = requests.get("http://104.211.219.98:80/train/trains",headers={
        'Authorization': f'Bearer {token}'
    })

    trains_data = get_trains.json()
    sorted_trains_data = sorted(trains_data, key=sort_key)
    return render_template('trains.html',sorted_trains_data=sorted_trains_data)

@app.route('/trains/<int:number>')
def get_train_info(number):
    post_req = requests.post(url, json=credentials)
    post_req_response =post_req.json()
    token =post_req_response["access_token"]

    get_train_details = requests.get(f"http://104.211.219.98:80/train/trains/{number}",headers={
        'Authorization': f'Bearer {token}'
    })
    train_data = get_train_details.json()
    print(train_data)
    return render_template("train_det.html",train=train_data)


if __name__ == '__main__':
    app.run(debug=True,port=3000)