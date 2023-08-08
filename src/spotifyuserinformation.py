import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from datetime import date


client_id = "1572e8f11a55483ba6336cc98058160e"
client_secret = "f6e304f95c1d41d1b3f9434437e88435"
redirect_uri = "http://localhost:8888/callback"

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri=redirect_uri, scope='user-top-read')
sp = spotipy.Spotify(auth_manager=auth_manager)

def getTopUserArtists(sp):
    results = sp.current_user_top_artists()

def getTopUserTracks(sp):