from flask import Flask
from flask import request
import logging
import requests
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

CLIENT_ID = '2180c40c536b5e5eb31a'
CLIENT_SECRET = '54a2853b9fff7e02c53c7aae4aad8d95390681c6'

@app.route('/')
def home_page():
    return f'<a href="https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://localhost:5000/oauth/redirect">login to GitHub</a>'

@app.route('/oauth/redirect')
def do_oauth():
    code = request.args.get('code')
    app.logger.info(f'got code: {code}')

    url = r'https://github.com/login/oauth/access_token'
    hdr = {"accept": 'application/json'}
    data = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "code" : code,
    }
    r = requests.post(url, json=data, headers=hdr)
    access_token = r.json()["access_token"]
    app.logger.info(f'got access token: {access_token}')
    
    url = r'https://api.github.com/user'
    hdr = {
        "accept": 'application/json',
        "Authorization": f'Bearer {access_token}'
    }
    r = requests.get(url, headers=hdr)
    jsn = r.json() 
    return f'你好，{jsn["login"]}'


if __name__ == '__main__':
    app.run()

