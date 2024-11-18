import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
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

def get_album_info(album_name, artist_name):
    """
    Searches Spotify for an album and returns its URI and genre.

    Args:
        album_name (str): The name of the album.
        artist_name (str): The name of the artist.

    Returns:
        tuple: A tuple containing the Spotify URI of the album and a list of genres,
               or (None, None) if not found.
    """

    query = f"album:{album_name} artist:{artist_name}"
    results = sp.search(q=query, type="album")

    try:
        album_uri = results['albums']['items'][0]['uri']
        # Handle potential KeyError for 'genres'
        genres = results['albums']['items'][0].get('genres', [])  # Return empty list if 'genres' not found
        return album_uri, genres
    except IndexError:
        return None, None

if __name__ == "__main__":
    # Import albums from CSV
    df_albums = pd.read_csv('albums.csv')  # Replace 'albums.csv' with your CSV file name

    album_data = []
    for index, row in df_albums.iterrows():
        album_name = row['album_name']
        artist_name = row['artist_name']
        album_uri, genres = get_album_info(album_name, artist_name)
        album_data.append({
            "album_name": album_name,
            "artist_name": artist_name,
            "album_uri": album_uri,
            "genres": genres
        })

    df = pd.DataFrame(album_data)
    print(df)