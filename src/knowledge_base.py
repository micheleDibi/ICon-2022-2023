import ast
import pyswip
import pandas as pd
from mapping_genres import map_genre_to_macro_category

prolog = pyswip.Prolog()
prolog.assertz("use_module(library(datetime))")

def escape_string(string):
    return string.replace("\"", '_').replace("'", '_')

def multi_assertz(pathList, assertzList):
    for path, assertz in zip(pathList, assertzList):
        df_temp = pd.read_csv(path)
        for index, row in df_temp.iterrows():
            prolog.assertz(f"{assertz}(\"{row['id']}\", {index+1})")

path_brani_preferiti = "./datasets/brani_preferiti_2023-08-11.csv"
path_artisti = "./datasets/artists_2023-08-11.csv"
path_album = "./datasets/albums_2023-08-11.csv"
path_artist_long_term = "./datasets/top_user_artists_long_term_2023-08-08.csv"
path_artist_mid_term = "./datasets/top_user_artists_medium_term_2023-08-08.csv"
path_artist_short_term = "./datasets/top_user_artists_short_term_2023-08-08.csv"
path_track_long_term = "./datasets/top_user_track_long_term_2023-08-08.csv"
path_track_mid_term = "./datasets/top_user_track_medium_term_2023-08-08.csv"
path_track_short_term = "./datasets/top_user_track_short_term_2023-08-08.csv"
path_clustering = "./datasets/clusteringDBSCAN.csv"

# Fatti per i brani
df_brani_preferiti = pd.read_csv(path_brani_preferiti)
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

multi_assertz([path_track_short_term, path_track_mid_term, path_track_long_term], ["brano_ascoltato_freq_short", "brano_ascoltato_freq_mid", "brano_ascoltato_freq_long"])

# Fatti per gli artisti
df_artists = pd.read_csv(path_artisti)
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
    
df_artist_clustering = pd.read_csv(path_clustering)
for index, row in df_artist_clustering.iterrows():
    prolog.assertz(f"macro_categoria_artista(\"{row['artist_id']}\", \"{row['cluster']}\")")
    
multi_assertz([path_artist_short_term, path_artist_mid_term, path_artist_long_term], ["artista_ascoltato_freq_short", "artista_ascoltato_freq_mid", "artista_ascoltato_freq_long"])

# Fatti per gli album
df_albums = pd.read_csv(path_album)
for index, row in df_albums.iterrows():
    prolog.assertz(f"album(\"{row['album_id']}\", \"{escape_string(row['album_name'])}\")")
    prolog.assertz(f"album(\"{row['album_id']}\", \"{row['album_release_date']}\")")

# Regole in Prolog
# Dato un artista di ottengono tutte le canzoni che ha fatto / Data una canzone di ottiene l'artista che l'ha fatta
prolog.assertz("ha_composto_canzone(IdArtista,IdCanzone) :- appartiene_album(IdCanzone,IdAlbum), ha_composto_album(IdArtista,IdAlbum)")

# Dato un album si ottengono tutti i suoi collaboratori / Dato un artista si ottengono tutti gli album in cui appare come collaboratore
prolog.assertz("collaboratore_album(IdAlbum, IdArtista) :- collaboratore_canzone(IdCanzone, IdArtista), appartiene_album(IdCanzone, IdAlbum)")
prolog.assertz("hanno_collaborato_album(IdArtista1,IdArtista2,IdAlbum) :- IdArtista1 \== IdArtista2, collaboratore_album(IdAlbum, IdArtista2), ha_composto_album(IdAlbum, IdArtista1)")
"""
prolog.assertz("hanno_collaborato_album(IdArtista1,IdArtista2,IdAlbum) :- ",
               "IdArtista1 \== IdArtista2, ",
               "collaboratori_album(IdAlbum, IdArtista1), ",
               "ha_composto_album(IdAlbum, IdArtista2)")
"""
prolog.assertz("hanno_collaborato_canzone(IdArtista1, IdArtista2, IdCanzone) :- IdArtista1 \== IdArtista2, collaboratore_canzone(IdCanzone, IdArtista2), ha_composto_canzone(IdArtista1, IdCanzone)")
prolog.assertz("hanno_collaborato_canzone(IdArtista1, IdArtita2, IdCanzone) :- IdArtista1 \== IdArtista2, collaboratore_canzone(IdCanzone, IdArtista1), collaboratore_canzone(IdCanzone, IdArtista2)")
prolog.assertz("simile_struttura_musicale(IdCanzone1,IdCanzone2) :- IdCanzone1 \== IdCanzone2, tonalita(IdCanzone1, Tonalita), tonalita(IdCanzone2, Tonalita), tempo(IdCanzone1, Tempo), tempo(IdCanzone2, Tempo), bpm(IdCanzone1, Bpm1), bpm(IdCanzone2,Bpm2), abs(Bpm1 - Bpm2) =< 15")
prolog.assertz("simili_per_emozioni(IdCanzone1, IdCanzone2) :- IdCanzone1 \== IdCanzone2, energia(IdCanzone1, Energia1), energia(IdCanzone2, Energia2), valenza(IdCanzone1, Valenza1), valenza(IdCanzone2, Valenza2), abs(Energia1 - Energia2) =< 20, abs(Valenza1,Valenza2) =< 0.3")
prolog.assertz("stesso_artista(IdCanzone1,IdCanzone2) :- IdCanzone1 \== IdCanzone2, ha_composto_canzone(IdArtista, IdCanzone1), ha_composto_canzone(IdArtista, IdCanzone2)")
prolog.assertz("stesso_album(IdCanzone1,IdCanzone2) :- IdCanzone1 \== IdCanzone2, appartiene_album(IdCanzone1,IdAlbum), appartiene_album(IdCanzone2, IdAlbum)")
prolog.assertz("stesso_genere_artista(IdArtista1, IdArtista2) :- IdArtista1 \== IdArtista2, genere_artista(IdArtista1,Genere), genere_artista(IdArtista2,Genere)")
prolog.assertz("collaborazione_successiva_album(IdArtista,IdAlbum,IdAlbum2) :- artista(IdArtista,NomeArtista), collaboratore_canzone(IdCanzone,Collaboratori), sub_atom(Collaboratori,_,_,_,NomeArtista), appartiene_album(IdCanzone,IdAlbum2), uscita_album(IdAlbum, DataUscita), uscita_album(IdAlbum2,DataUscita2), DataUscita < DataUscita2")
prolog.assertz("collaborazione_precedente_album(IdArtista,IdAlbum,IdAlbum2) :- artista(IdArtista,NomeArtista), collaboratore_canzone(IdCanzone,Collaboratori), sub_atom(Collaboratori,_,_,_,NomeArtista), appartiene_album(IdCanzone,IdAlbum2), uscita_album(IdAlbum, DataUscita), uscita_album(IdAlbum2,DataUscita2), DataUscita > DataUscita2")

def generi_preferiti(pathList):
    generi = {}
    weights = [0.2, 0.4, 1, 0.2, 0.4, 1]
    
    for path, weight in zip(pathList, weights):
        print(path)
        df = pd.read_csv(path)
        
        for index, row in df.iterrows():
            query = ""
            
            if 'track' in path:
                query = f"genere_artista(Artista_id, Genere), ha_composto_canzone(Artista_id, \"{row['id']}\")"
            else :
                query = f"genere_artista(\"{row['id']}\", Genere)"
            
            genres = list(prolog.query(query))
            
            for genre in genres:
                if genre['Genere'].decode("ASCII") in generi:
                    generi[f"{genre['Genere'].decode('ASCII')}"] += (1 * weight) + (1 - ((index + 1) / len(df)))
                else:
                    generi[f"{genre['Genere'].decode('ASCII')}"] = (1 * weight) + (1 - ((index + 1) / len(df)))
    
    return generi
            
generi_preferiti([path_track_short_term, path_track_mid_term, path_track_long_term, path_artist_short_term, path_artist_mid_term, path_artist_long_term])