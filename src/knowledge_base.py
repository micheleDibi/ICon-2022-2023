import ast
import pyswip
import pandas as pd
from mapping_genres import map_genre_to_macro_category

prolog = pyswip.Prolog()
prolog.assertz("use_module(library(datetime))")

def escape_string(string):
    return string.replace("\"", '_').replace("'", '_')

# Fatti per i brani
df_brani_preferiti = pd.read_csv("./datasets/brani_preferiti_2023-08-11.csv")
df_brani_preferiti['side_artists_id'] = df_brani_preferiti['side_artists_id'].apply(ast.literal_eval)  
check_duplicates = False
for index, row in df_brani_preferiti.iterrows():
    check_artista_album = False
    
    prolog.assertz(f"nome_canzone(\"{row['track_id']}\", \"{escape_string(row['track_name'])}\")")
    prolog.assertz(f"popolarita(\"{row['track_id']}\", {row['track_popularity']})")
    prolog.assertz(f"tonalita(\"{row['track_id']}\", {row['track_key']})")
    prolog.assertz(f"bpm(\"{row['track_id']}\", {row['track_bpm']})")
    prolog.assertz(f"energia(\"{row['track_id']}\", {row['track_energy']})")
    prolog.assertz(f"acustica(\"{row['track_id']}\", {row['track_acousticness']})")
    prolog.assertz(f"stumentalita(\"{row['track_id']}\", \"{row['track_instrumentalness']}\")")
    prolog.assertz(f"mode(\"{row['track_id']}\", \"{row['track_mode']}\")")
    prolog.assertz(f"tempo(\"{row['track_id']}\", \"{row['track_time_signature']}\")")
    prolog.assertz(f"valenza(\"{row['track_id']}\", {row['track_happiness']})")

    prolog.assertz(f"appartiene_album(\"{row['track_id']}\", \"{row['album_id']}\")")
    
    for side_artist in row['side_artists_id']:
        prolog.assertz(f"collaboratore_canzone(\"{row['track_id']}\", \"{side_artist}\")")
    
    if check_duplicates:
        results = list(prolog.query(f"ha_composto_album(\"{row['main_artist_id']}\", Album_id)"))
        for album in results:
            if album['Album_id'].decode("ASCII") == row['album_id']:
                check_artista_album = True
                break
            
    if not(check_artista_album):
        check_duplicates = True
        prolog.assertz(f"ha_composto_album(\"{row['main_artist_id']}\", \"{row['album_id']}\")")
    
    
# Fatti per gli artisti
df_artists = pd.read_csv("./datasets/artists_2023-08-11.csv")
df_artists['artist_genres'] = df_artists['artist_genres'].apply(ast.literal_eval)  

for index, row in df_artists.iterrows():
        macro_genres = []
    
        for genre in row['artist_genres']:
            macro_genres.append(map_genre_to_macro_category(genre))
    
        df_artists.at[index, 'artist_genres'] = list(set(macro_genres))

for index, row in df_artists.iterrows():
    prolog.assertz(f"artista(\"{row['artist_id']}\", \"{row['artist_name']}\")")
    
    for genre in row['artist_genres']:
        prolog.assertz(f"genere_artista(\"{row['artist_id']}\", \"{genre}\")")
    
# Fatti per gli album
df_albums = pd.read_csv("./datasets/albums_2023-08-11.csv")
for index, row in df_albums.iterrows():
    prolog.assertz(f"album(\"{row['album_id']}\", \"{escape_string(row['album_name'])}\")")
    prolog.assertz(f"album(\"{row['album_id']}\", \"{row['album_release_date']}\")")


"""
% Template Fatti
% canzone("id", "nomeCanzone").
% appartiene_album("idCanzone", "idAlbum").
% artista("idArtista","nomeArtista")
% genere_artista("idArtista", "generi").
% popolarita("id", valore).
% tonalita("id", valore).
% bpm("id", valore).
% energia("id", valore).
% acustica("id", valore).
% strumentalita("id", valore).
% mode("id",valore).
% tempo("id", valore).
% valenza("id", valore).

% album("idAlbum", "nomeAlbum").
% ha_composto_album("idArtista", "idAlbum").
% uscita_album("idAlbum", valore).
"""