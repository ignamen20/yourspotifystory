from flask import Flask, request, url_for, session, redirect, render_template, g
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from groq import Groq 
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

@app.route('/')
def welcome():
    if client_id and client_secret:
        print("Client ID and Client Secret loaded successfully.")
    else:
        print("Error: Client ID or Client Secret not loaded.")
    print(f"Client ID: {client_id}, Client Secret: {client_secret}")
    return render_template('welcome.html')

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

@app.route('/top_songs')
def get_top_songs():
    session['chosen_scope'] = "user-top-read"
    sp_oauth = create_spotify_oauth(session.get('chosen_scope', None))
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/getTopTracks', methods=['POST', 'GET'])
def getTopTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged")
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    limit_chosen = 3
    song_item = sp.current_user_top_tracks(
        limit=limit_chosen, offset=19, time_range='long_term')['items']
    client = Groq(
    api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
    messages=[
            {
            "role": "user",
            "content": """You are a psychiatrist specialised in finding as much about people as possible knowing only what music they listen to. 
I want you to write a personality analysis about a person knowing only their favourite songs. I want you to use the lyrics of the songs they listen to the most to understand what they are feeling and what they have gone through. Also you can make inferences about what they should expect in the future.
The tone used in the analysis should be professional and confident in what you're saying. 
The user is a person curious about what their songs say about them. They want to feel surprised as to how you can tell them just from their songs and they want to feel special.
The first paragraph should be 50 words long and contain most of the inferences, without going into detail on how you came to them. In this first paragraph I also want you to say what they are going through currently.
In the rest of the paragraphs I want you to quote the song titles and part of the lyrics to support the assumptions you make.
The complete analysis should be around 250 words long. Write it in Spanish.
The songs are:"""+
song_item[0]['name'] + " by " + song_item[0]['artists'][0]['name'] + ", " 
,
        }
    ],
    model="llama3-8b-8192",
)
    return render_template('show_analysis.html', analysis=chat_completion.choices)


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