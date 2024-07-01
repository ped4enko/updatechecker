
#cd ~/Downloads/development/updatechecker/
#source venv/bin/activate
#pip install flask-cors
#python3 app.py

#cd client
#npm start

from flask import Flask, redirect, request, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Читайте облікові дані з JSON файлу
client_secrets_file = 'client_secret_89035735250-4i8atddr55e9o44idm2rlc854r9e9n32.apps.googleusercontent.com.json'
with open(client_secrets_file) as f:
    client_secrets = json.load(f)

REDIRECT_URI = 'http://localhost:5001/callback'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
flow = Flow.from_client_config(
    client_secrets,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route('/')
def home():
    return 'Welcome to Google Update Checker!'

@app.route('/auth')
def auth():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    return redirect(f'http://localhost:3000?token={credentials.token}')

@app.route('/sites')
def sites():
    try:
        token = request.args.get('token')
        credentials = flow.credentials
        credentials.token = token
        service = build('webmasters', 'v3', credentials=credentials)
        site_list = service.sites().list().execute()

        return jsonify(site_list)
    except Exception as e:
        print(f"Error fetching sites: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/data')
def data():
    try:
        token = request.args.get('token')
        site_url = request.args.get('siteUrl')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        compare_start_date = request.args.get('compareStartDate')
        compare_end_date = request.args.get('compareEndDate')

        credentials = flow.credentials
        credentials.token = token
        service = build('webmasters', 'v3', credentials=credentials)

        response_current = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': ['date']
            }
        ).execute()

        response_compare = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                'startDate': compare_start_date,
                'endDate': compare_end_date,
                'dimensions': ['date']
            }
        ).execute()

        return jsonify({
            "current": response_current,
            "compare": response_compare
        })
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)