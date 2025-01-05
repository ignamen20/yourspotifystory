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
    if client_id and client_secret:
        print("Client ID and Client Secret loaded successfully.")
    else:
        print("Error: Client ID or Client Secret not loaded.")
    print(f"Client ID: {client_id}, Client Secret: {client_secret}")
    if groq_api_key:
        print("Groq API Key loaded successfully.")
    else:
            print("Error: Groq API Key not loaded.") 
    if openai_api_key:
        print("OpenAI API Key loaded successfully.")   
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
    limit_chosen = 20
    song_item_long_term = sp.current_user_top_tracks(
        limit=limit_chosen, offset=0, time_range='long_term')['items']
    song_item_medium_term = sp.current_user_top_tracks(
        limit=limit_chosen, offset=0, time_range='medium_term')['items']
    song_item_short_term = sp.current_user_top_tracks(
        limit=limit_chosen, offset=0, time_range='short_term')['items']
    long_term_songs = (
    song_item_long_term[0]['name'] + " by " + song_item_long_term[0]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[0]['popularity']) + ", " +
    song_item_long_term[1]['name'] + " by " + song_item_long_term[1]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[1]['popularity']) + ", " +
    song_item_long_term[2]['name'] + " by " + song_item_long_term[2]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[2]['popularity']) + ", " +
    song_item_long_term[3]['name'] + " by " + song_item_long_term[3]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[3]['popularity']) + ", " +
    song_item_long_term[4]['name'] + " by " + song_item_long_term[4]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[4]['popularity']) + ", " +
    song_item_long_term[5]['name'] + " by " + song_item_long_term[5]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[5]['popularity']) + ", " +
    song_item_long_term[6]['name'] + " by " + song_item_long_term[6]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[6]['popularity']) + ", " +
    song_item_long_term[7]['name'] + " by " + song_item_long_term[7]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[7]['popularity']) + ", " +
    song_item_long_term[8]['name'] + " by " + song_item_long_term[8]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[8]['popularity']) + ", " +
    song_item_long_term[9]['name'] + " by " + song_item_long_term[9]['artists'][0]['name'] + ' pop=' + str(song_item_long_term[9]['popularity']) + "."
)
    medium_term_songs = (
    song_item_medium_term[0]['name'] + " by " + song_item_medium_term[0]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[0]['popularity']) + ", " +
    song_item_medium_term[1]['name'] + " by " + song_item_medium_term[1]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[1]['popularity']) + ", " +
    song_item_medium_term[2]['name'] + " by " + song_item_medium_term[2]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[2]['popularity']) + ", " +
    song_item_medium_term[3]['name'] + " by " + song_item_medium_term[3]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[3]['popularity']) + ", " +
    song_item_medium_term[4]['name'] + " by " + song_item_medium_term[4]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[4]['popularity']) + ", " +
    song_item_medium_term[5]['name'] + " by " + song_item_medium_term[5]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[5]['popularity']) + ", " +
    song_item_medium_term[6]['name'] + " by " + song_item_medium_term[6]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[6]['popularity']) + ", " +
    song_item_medium_term[7]['name'] + " by " + song_item_medium_term[7]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[7]['popularity']) + ", " +
    song_item_medium_term[8]['name'] + " by " + song_item_medium_term[8]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[8]['popularity']) + ", " +
    song_item_medium_term[9]['name'] + " by " + song_item_medium_term[9]['artists'][0]['name'] + ' pop=' + str(song_item_medium_term[9]['popularity']) + "."
    )
    short_term_songs = (
    song_item_short_term[0]['name'] + " by " + song_item_short_term[0]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[0]['popularity']) + ", " +
    song_item_short_term[1]['name'] + " by " + song_item_short_term[1]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[1]['popularity']) + ", " +
    song_item_short_term[2]['name'] + " by " + song_item_short_term[2]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[2]['popularity']) + ", " +
    song_item_short_term[3]['name'] + " by " + song_item_short_term[3]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[3]['popularity']) + ", " +
    song_item_short_term[4]['name'] + " by " + song_item_short_term[4]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[4]['popularity']) + ", " +
    song_item_short_term[5]['name'] + " by " + song_item_short_term[5]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[5]['popularity']) + ", " +
    song_item_short_term[6]['name'] + " by " + song_item_short_term[6]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[6]['popularity']) + ", " +
    song_item_short_term[7]['name'] + " by " + song_item_short_term[7]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[7]['popularity']) + ", " +
    song_item_short_term[8]['name'] + " by " + song_item_short_term[8]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[8]['popularity']) + ", " +
    song_item_short_term[9]['name'] + " by " + song_item_short_term[9]['artists'][0]['name'] + ' pop=' + str(song_item_short_term[9]['popularity']) + "."
    )
    #sadly, they deprecated the audio features endpoint
    #features = sp.audio_features(id_list)
    #song_list =[]
    # for i in range(limit_chosen):
    #         songs_values = {
    #             'song_name':song_item[i]['name'],
    #             'song_artist':song_item[i]['artists'][0]['name'],
    #             'song_album':song_item[i]['album']['name'],
    #             'song_popularity':song_item[i]['popularity'],
    #             'accousticness':features[i]['acousticness'],
    #             'danceability':features[i]['danceability'],
    #             'duration_ms':features[i]['duration_ms'],
    #             'energy':features[i]['energy'],
    #             'instrumentalness':features[i]['instrumentalness'],
    #             'key':features[i]['key'],
    #             'liveness':features[i]['liveness'],
    #             'loudness':features[i]['loudness'],
    #             'mode':features[i]['mode'],
    #             'speechiness':features[i]['speechiness'],
    #             'tempo':features[i]['tempo'],
    #             'time_signature':features[i]['time_signature'],
    #             'valence':features[i]['valence']
    #         }
    #         song_list.append(songs_values)
    #average_danceability = calculate_average('danceability', song_list)
    client = OpenAI(
        api_key=openai_api_key
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": '''You are a psychiatrist specialised in doing personality analysis based on people's music taste.
            The tone used in the analysis should be professional and confident in what you're saying.
            The user is a person curious about what their songs say about them. They want to feel surprised as to how you can tell them just from their songs and they want to feel special.
            I will give you the top 10 songs this person has listened to in the long, medium and short term. I want you to analyse the themes of the songs, the lyrics and give conclusions.
            The first paragraph will be a summary of all your conclusions, which I will list in the following points:
            1. What the person overall listens to. Happy songs, sad songs, instrumental songs, very popular songs, etc.
            2. What the person is going through currently.
            For example, if the person listens to a lot of happy songs in the long term, but in the short term has gotten into more sad, slow songs, you will say that they're going through a rough patch.
            3. Talk about the popularity of the songs. I want you to analyse 2 things: if the average popularity of the songs is high, but there is one song that is very unpopular, or vice versa, I want you to point that out, and say for example "This person listens to popular songs, with the exeption of this particular song
            Also, if the average popularity of the long term songs is high, but in the short term they are listening to less popular songs, I want you to point that out.
            Support your claims using part of the song's lyrics and song names. Make it around 300 words long.
            ''' + "."+
            "The long-term songs are "+ long_term_songs
            + "The medium-term songs are "+ medium_term_songs
            + "The short-term songs are "+ short_term_songs
        }
    ]
)
#     client = Groq(
#     api_key=groq_api_key)
#     chat_completion = client.chat.completions.create(
#     messages=[
#             {
#             "role": "user",
#             "content": """You are a psychiatrist specialised in finding as much about people as possible knowing only what music they listen to. 
# I want you to write a personality analysis about a person knowing only their favourite songs. I want you to use the lyrics of the songs they listen to the most to understand what they are feeling and what they have gone through. Also you can make inferences about what they should expect in the future.
# The tone used in the analysis should be professional and confident in what you're saying. 
# The user is a person curious about what their songs say about them. They want to feel surprised as to how you can tell them just from their songs and they want to feel special.
# The first paragraph should be 50 words long and contain most of the inferences, without going into detail on how you came to them. In this first paragraph I also want you to say what they are going through currently.
# In the rest of the paragraphs I want you to quote the song titles and part of the lyrics to support the assumptions you make.
# The complete analysis should be around 250 words long. Write it in Spanish. Include the name of the three songs.
# The songs are:"""+
# song_item[0]['name'] + " by " + song_item[0]['artists'][0]['name'] + ", " 
# ,
#         }
#     ],
#     model="llama3-8b-8192",
# )
    #return long_term_songs + "\n" + medium_term_songs + "\n" + short_term_songs
    #return completion.choices[0].message.content
    return render_template('show_analysis.html', analysis=completion.choices)


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

def calculate_average(feature_name, song_list):
    total = sum(song[feature_name] for song in song_list)
    count = len(song_list)
    return total / count if count > 0 else 0

if __name__ == '__main__':
    app.run()  