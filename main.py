from flask import Flask
import requests
from dotenv import load_dotenv
import os

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

