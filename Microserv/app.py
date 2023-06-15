from flask import Flask
import requests

app = Flask(__name__)

@app.route('/numbers',methods=['GET'])
def nums():
    url_list = requests.args.getlist('url')