import pandas as pd
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='YOUR_CLIENT_ID',
                                                           client_secret='YOUR_CLIENT_SECRET'))

def get_album_uri(album_name, artist_name):
    """
    Searches Spotify for an album and returns its URI.
    """
    try:
        results = sp.search(q=f'album:{album_name} artist:{artist_name}', type='album')
        return results['albums']['items'][0]['uri']
    except IndexError:
        print(f"Album not found on Spotify: {album_name} by {artist_name}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while searching for the album: {e}")
        return None

def get_songs_from_album(album_uri):
    """
    Retrieves song URIs and names from a given album URI.
    """
    songs = []
    try:
        results = sp.album_tracks(album_uri)
        for track in results['items']:
            songs.append((track['uri'], track['name']))
        return songs
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred while fetching songs from the album: {e}")
        return None

def store_album_and_songs(album_name, artist_name, album_uri, songs, cursor):
    """
    Stores album and song data in the database.
    """
    try:
        cursor.execute("INSERT OR IGNORE INTO albums (album_name, artist_name, album_uri) VALUES (?, ?, ?)",
                       (album_name, artist_name, album_uri))
        if songs:
            for song_uri, song_name in songs:
                cursor.execute("INSERT OR IGNORE INTO songs (album_uri, song_uri, song_name) VALUES (?, ?, ?)",
                               (album_uri, song_uri, song_name))
    except sqlite3.Error as e:
        print(f"An error occurred while storing data in the database: {e}")

if __name__ == "__main__":
    conn = sqlite3.connect('melodi.db')
    cursor = conn.cursor()

    # Create the albums table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            album_name TEXT, 
            artist_name TEXT, 
            album_uri TEXT PRIMARY KEY
        )
    ''')

    # Create the songs table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            album_uri TEXT,
            song_uri TEXT PRIMARY KEY,
            song_name TEXT
        )
    ''')

    try:
        df_albums = pd.read_csv('albums.csv')
        for _, row in df_albums.iterrows():
            album_name = row['album_name']
            artist_name = row['artist_name']

            album_uri = get_album_uri(album_name, artist_name)
            if album_uri:
                songs = get_songs_from_album(album_uri)
                if songs:
                    store_album_and_songs(album_name, artist_name, album_uri, songs, cursor)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    conn.commit()
    conn.close()