import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from airflow.models import Variable


# Generate your token here:  https://developer.spotify.com/console/get-recently-played/
# Note: You need a Spotify account (can be easily created for free)

# def check_if_valid_data(df: pd.DataFrame) -> bool:
#     # Check if dataframe is empty
#     if df.empty:
#         print("No songs downloaded. Finishing execution")
#         return False 

#     # Primary Key Check
#     if pd.Series(df['played_at']).is_unique:
#         pass
#     else:
#         raise Exception("Primary Key check is violated")

#     # Check for nulls
#     if df.isnull().values.any():
#         raise Exception("Null values found")

#     # Check that all timestamps are of yesterday's date
#     yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
#     yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

#     timestamps = df["timestamp"].tolist()
#     for timestamp in timestamps:
#         if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
#             raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

#     return True


def run_spotify_etl():
    DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
    USER_ID = ''
    TOKEN = Variable.get("spotify_token")

      # Extract part of the ETL process
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy/tracks", headers = headers)

    data = r.json()

    song_names = []
    artist_names = []


    # Extracting only the relevant bits of data from the json object      
    for song in data['items']:
       artist_names.append(song['artists'][0]['name'])
       song_names.append(song['name'])

       song_dict = {
              "artist_name" : artist_names,
                "song_name" : song_names,
       }
    

    song_df = pd.DataFrame(song_dict, columns = ['artist_name', 'song_name'])
    print(song_df)
    
    # Validate
    # if check_if_valid_data(song_df):
    #     print("Data valid, proceed to Load stage")

    # Load

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")


run_spotify_etl()