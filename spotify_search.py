import spotipy # Install with `pip install spotipy`
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
load_dotenv()


# Set up your Spotify API credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


# Authenticate with the Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_info(spotify_url):
    try:
        track_id = spotify_url.split('/')[-1].split('?')[0]
        track = sp.track(track_id)
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        return track_name, artist_name
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    spotify_url = input("Enter Spotify URL: ")
    track_name, artist_name = get_track_info(spotify_url)
    if track_name and artist_name:
        print(f"Track Name: {track_name}")
        print(f"Artist Name: {artist_name}")
    else:
        print("Could not retrieve track information.")