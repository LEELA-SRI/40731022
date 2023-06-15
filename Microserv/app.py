from flask import Flask,jsonify,request,render_template
import requests
from urllib.parse import urlparse

app = Flask(__name__)
@app.route('/')
def home():
    return 'hello'
@app.route('/numbers',methods=['GET'])
def nums():
    url_list = request.args.getlist('url')
    num_list = set()
    for url in url_list:
        try:
            server_response = requests.get(url,timeout=10)

            if server_response.status_code == 200:
                get_data = server_response.json()
                if get_data['numbers'] :
                    num_list.update(get_data['numbers'])
        except  requests.exceptions.Timeout:
            return {'message': 'Request Timed out'}

    sorted_unique = sorted(num_list)
    
    return render_template('index.html',sorted_unique=sorted_unique)

if __name__ == '__main__':
    app.run(debug=True,port=3000)
