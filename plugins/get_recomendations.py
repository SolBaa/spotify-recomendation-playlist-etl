# 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA'
# curl --request GET \
#   --url 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA' \

# curl --request GET \
#   --url https://api.spotify.com/v1/me/top/artists \

# BQAD9cUflfgsa-FUFg5hTvDxACuJrVOsQjtVul9NMjVWJOIqp5UQKLa_f_iG94vNr2FgchlNwsVoBcA1DvA1XuItEFLSCBLu0u2RAdGifzVHh7msHWE

## GET TOP ARTISTS

## GET TOP TRACKS

## GET RECOMMENDATIONS

## CREATE PLAYLIST

## ADD SONGS TO PLAYLIST


import webbrowser
import requests
import base64
from urllib.parse import urlencode, quote_plus, urlparse, parse_qs

import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests

from http.server import BaseHTTPRequestHandler, HTTPServer
import configparser

# load the postgres_config values
parser = configparser.ConfigParser()
parser.read("auth.conf")

client_id = parser.get('spotify', 'client_id')
redirect_uri = parser.get('spotify', 'redirect_uri')
client_secret = parser.get('spotify', 'client_secret')

# Define the scopes your application is requesting
scopes = 'user-follow-read'



# function to get the authorization code
def get_auth_code(self):
    query = urlparse(self.path).query
    auth_code = parse_qs(query)['code'][0]
    return auth_code

# function to get the access token
def get_access_token(auth_code):
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token

# function to get artist data
def get_artist_data(access_token):
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}",
        'Scope' : 'user-follow-read'
    }

    r = requests.get("https://api.spotify.com/v1/me/following?type=artist", headers=headers)
    data = r.json()

    artist_ids = [artist['id'] for artist in data['artists']['items']]

    return artist_ids

# function to get top artist data
def get_top_artist_data(access_token,artists_id):
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }

    artist_df = []
    for artist_id in artists_id:
        r = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers)
        data = r.json()

        artist_name = data['name']
        artist_id = data['id']
        artist_popularity = data['popularity']
        artist_followers =  data['followers']['total']
        artist_genres = data['genres']
 

        artist_dict = {
            'artist_name' : artist_name,
            'artist_id' : artist_id,
            'artist_popularity' : artist_popularity,
            'artist_followers' : artist_followers,
            'artist_genres' : artist_genres
        }
        artist_df.append(artist_dict)

    # artist_df = pd.DataFrame(artist_dict,columns=['artist_name','artist_id','artist_popularity','artist_followers','artist_genres'] )
    ar_df = pd.DataFrame(artist_df, columns=['artist_name','artist_id','artist_popularity','artist_followers','artist_genres'])
    return ar_df
        



# handler for the server
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'You can close this window')

        auth_code = get_auth_code(self)
        access_token = get_access_token(auth_code)
        artist_ids = get_artist_data(access_token)
        artist_data = get_top_artist_data(access_token,artist_ids)

        # print(f"Your access token is: {access_token}")
        # print(f"Artist IDs: {artist_ids}")
        print(f"Artist Data: {artist_data}")

# function to open the authorization URL in the browser
def open_auth_url():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scopes
    }

    url_params = urlencode(params)
    auth_url = f"https://accounts.spotify.com/authorize?{url_params}"

    webbrowser.open(auth_url)

# run the server
def run_server():
    server = HTTPServer(('localhost', 8080), RequestHandler)
    server.handle_request()

# main program flow
def main():
    open_auth_url()
    run_server()

if __name__ == "__main__":
    main()