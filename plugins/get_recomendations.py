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

import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from airflow.models import Variable


def run_spotify_recomendation():
    DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
    # TOKEN = Variable.get("spotify_token")
    # TOKEN = 'BQB5BKqX3O58ysVd9ygz57ayZ7EwxX6E0VhcPmgsUJHElfXs4Ev37-M08hMuOo35bt4FLuxlYaqN_28YIRFa38GgMybkEGK3mKGwjFcGO0a0gzq7OBo'
    TOKEN= 'BQANvofB_QoLUAHzB_r2IdbMuKWEsSD6KvjiwnIEJyfp1c3begb46uGLujUEXUKPjYUQszBSm2dcnctcvKnB3TuSPzSwSNrlRgDm5DBr3b883MklZqT2Y0ibHwQ'

      # Extract part of the ETL process
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN),
        'Scope' : 'user-follow-read'
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/following?type=artist", headers = headers)

    data = r.json()
    print(data)

    # song_names = []
    artist_id = []


    # Extracting only the relevant bits of data from the json object      
    # for artist in data['items']:
    #    artist_id.append(artist['id'])
    #    song_names.append(song['name'])

    #    song_dict = {
    #           "artist_name" : artist_names,
    #             "song_name" : song_names,
    #    }
    

    # song_df = pd.DataFrame(song_dict, columns = ['artist_name', 'song_name'])
    print(artist_id)
run_spotify_recomendation()
    
    # Validate
    # if check_if_valid_data(song_df):
    #     print("Data valid, proceed to Load stage")

    # Load

    # engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    # conn = sqlite3.connect('my_played_tracks.sqlite')
    # cursor = conn.cursor()

    # sql_query = """
    # CREATE TABLE IF NOT EXISTS my_played_tracks(
    #     song_name VARCHAR(200),
    #     artist_name VARCHAR(200)
    # )
    # """

    # cursor.execute(sql_query)
    # print("Opened database successfully")

    # try:
    #     song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    # except:
    #     print("Data already exists in the database")

    # conn.close()
    # print("Close database successfully")