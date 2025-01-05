from flask import Flask, request, url_for, session, redirect, render_template, g
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from groq import Groq 
from openai import OpenAI
import time
import os
import sys
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

app.secret_key = "generate_it_on_the_fly"
app.config['SESSION_COOKIE_NAME'] = 'Ignas Cookie'
TOKEN_INFO = 'token_info'

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
groq_api_key = os.getenv("GROQ_API_KEY")
openai_project_id = os.getenv("OPENAI_PROJECT_ID")
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/getTopTracks', methods=['POST', 'GET'])
def getTopTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged")
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    limit_chosen = 10
    song_item = sp.current_user_top_tracks(
        limit=limit_chosen, offset=0, time_range='long_term')['items']
    id_list = []
    for i in range(len(song_item)):
        id_list.append(song_item[i]['id'])
    #features = sp.audio_features(id_list)
    song_list =[]
    return sp.audio_analysis(str(song_item[0]['id']))

@app.route('/top_songs')
def get_top_songs():
    session['chosen_scope'] = "user-top-read"
    sp_oauth = create_spotify_oauth(session.get('chosen_scope', None))
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth(session.get('chosen_scope', None))
    if session.get('chosen_scope', None) == "user-top-read":
        redirect_url = 'getTopTracks'
    if session.get('chosen_scope', None) == "user-library-read":
        redirect_url = 'getSavedTracks'
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    print('this is running')
    return redirect(url_for(redirect_url, _external=True))

def create_spotify_oauth(desired_scope):
    return SpotifyOAuth(
        client_id,
        client_secret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope='user-library-read user-top-read')


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("No token info found")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth(session.get('chosen_scope', None))
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

if __name__ == '__main__':
    app.run()  