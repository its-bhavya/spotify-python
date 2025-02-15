from flask import Flask, redirect
import requests
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

app = Flask(__name__)
app.secret_key= "123456789-9891695800"

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')

REDIRECT_URI='http://localhost:8000/'

AUTH_URL='https://accounts.spotify.com/authorize'
TOKEN_URL='https://accounts.spotify.com/api/token'
API_BASE_URL='https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome! <a href = '/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-email user-read-private' 

    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code':request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token']=token_info['access_token']
        session['refresh_token']=token_info['refresh_token']
        session['expires_at']=datetime.now() + token_info['expires_in'] 

        return redirect('/playlists')

@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)

    platlists = response.json()

    return jsonify(playlists)
    
