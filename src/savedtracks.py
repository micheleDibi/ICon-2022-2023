import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
from datetime import date

client_id = "1572e8f11a55483ba6336cc98058160e"
client_secret = "f6e304f95c1d41d1b3f9434437e88435"
redirect_uri = "http://localhost:8888/callback"

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri=redirect_uri, scope='user-library-read')
sp = spotipy.Spotify(auth_manager=auth_manager)

offset = 0
limit = 50

saved_tracks = []
artists = []
albums = []

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    tracks = results['items']

    if not tracks:
        break

    for track in tracks:
        added_at = track['added_at']
        track = track['track']
        features = sp.audio_features(track['id'])
        
        if features[0] != None:
            
            print(track['name'])

            artist_result = sp.artist(track['artists'][0]['id'])
            current_artist = {
                'artist_id': track['artists'][0]['id'],
                'artist_name': track['artists'][0]['name'],
                'artist_followers': artist_result['followers']['total'],
                'artist_genres': artist_result['genres'],
                'artist_popularity': artist_result['popularity']
            }            
            artists.append(current_artist)

            side_artists = []
            for side_artist in track['artists'][1:]:
                
                artist_result = sp.artist(side_artist['id'])
                
                current_artist = {
                    'artist_id': side_artist['id'],
                    'artist_name': side_artist['name'],
                    'artist_followers': artist_result['followers']['total'],
                    'artist_genres': artist_result['genres'],
                    'artist_popularity': artist_result['popularity']
                }
                
                side_artists.append(side_artist['id'])
            
            album_result = sp.album(track['album']['id'])
            
            current_album = {
                'album_id': track['album']['id'],
                'album_name': track['album']['name'],
                'album_total_tracks': track['album']['total_tracks'],
                'album_type': track['album']['album_type'],
                'album_release_date': track['album']['release_date'],
                # 'album_genres': album_result['genres'],
                'album_label': album_result['label'],
                'album_popularity': album_result['popularity']
            }    
            
            albums.append(current_album)
            
            """
            current_track = {
                'id': track['id'],
                'added_at': added_at,
                'name': track['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'main_artist': track['artists'][0]['name'], 
                'side_artists': side_artists,
                'popularity': track['popularity'],
                'key': features[0]['key'],
                'bpm': round(features[0]['tempo']),
                'energy': round(features[0]['energy'], 2),
                'danceability': round(features[0]['danceability'], 2),
                'happiness': round(features[0]['valence'], 2),
                'loudness': round(features[0]['loudness'], 2),
                'acousticness': round(features[0]['acousticness'], 2),
                'instrumentalness': round(features[0]['instrumentalness'], 2),
                'liveness': round(features[0]['liveness'], 2),
                'mode': features[0]['mode'],
                'speechiness': round(features[0]['speechiness'], 3),
                'time_signature': features[0]['time_signature']
            }
            """
            current_track = {
                'track_id': track['id'],
                'track_added_at': added_at,
                'track_name': track['name'],
                'album_id': track['album']['id'],
                'main_artist_id': track['artists'][0]['id'], 
                'side_artists_id': side_artists,
                'track_duration': track['duration_ms'],
                'track_explicit': track['explicit'],
                'track_popularity': track['popularity'],
                'track_key': features[0]['key'],
                'track_bpm': features[0]['tempo'],
                'track_energy': features[0]['energy'],
                'track_danceability': features[0]['danceability'],
                'track_happiness': features[0]['valence'],
                'track_loudness': features[0]['loudness'],
                'track_acousticness': features[0]['acousticness'],
                'track_instrumentalness': features[0]['instrumentalness'],
                'track_liveness': features[0]['liveness'],
                'track_mode': features[0]['mode'],
                'track_speechiness': features[0]['speechiness'],
                'track_time_signature': features[0]['time_signature']
            }
            
            saved_tracks.append(current_track)
        
    offset += limit

df_saved_tracks = pd.DataFrame(saved_tracks)
df_saved_tracks.to_csv(f"saved_tracks_{date.today()}.csv", index=False)

df_albums = pd.DataFrame(albums)
df_albums = df_albums.drop_duplicates(subset="album_id")
df_albums.to_csv(f"albums_{date.today()}.csv", index=False)

df_artists = pd.DataFrame(artists)
df_artists = df_artists.drop_duplicates(subset="artist_id")
df_artists.to_csv(f"artists_{date.today()}.csv", index=False)