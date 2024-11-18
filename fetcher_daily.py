import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Spotify API credentials
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

# Spotify authorization
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/",
                                               scope=scope))


def update_song_popularity():
    """
    Fetches the current popularity for each song in the 'songs' table and updates the database.
    """
    try:
        conn = sqlite3.connect('melodi.db')
        cursor = conn.cursor()

        # Fetch all song URIs from the 'songs' table
        cursor.execute("SELECT song_uri FROM songs")
        song_uris = cursor.fetchall()

        for (song_uri,) in song_uris:
            try:
                # Fetch the current popularity from Spotify API
                popularity = sp.track(song_uri)['popularity']

                # Update the 'songs' table with the current popularity
                cursor.execute("UPDATE songs SET popularity = ? WHERE song_uri = ?", (popularity, song_uri))

            except spotipy.exceptions.SpotifyException as e:
                print(f"An error occurred while fetching song popularity: {e}")

        conn.commit()
        print("Song popularity updated successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred while updating song popularity: {e}")
    finally:
        if conn:
            conn.close()

# Schedule the update_song_popularity function to run daily
schedule.every().day.at("00:00").do(update_song_popularity)  # Runs every day at midnight

while True:
    schedule.run_pending()
    time.sleep(1)