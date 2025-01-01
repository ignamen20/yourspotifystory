<<<<<<< HEAD
from flask import Flask
app = Flask(__name__)

@app.route('/') 
def hello_world():
    return 'Tengo un sitio web, idiota'
=======
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
print(client_id)


@app.route('/')
def welcome():
    print(client_id,client_secret)
    return render_template('welcome.html')
>>>>>>> 1a0ec4e (subo primera inclusion de compu HP)

if __name__ == '__main__':
    app.run()  