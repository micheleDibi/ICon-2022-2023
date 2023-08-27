
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from knowledge_base import KB

prolog = KB()
df_brani = pd.read_csv("./datasets/brani_preferiti_2023-08-11.csv")

def rimuovi_simboli_speciali(input_string):
    stringa_pulita = re.sub(r'\([^)]*\)', '', input_string)
    stringa_pulita = re.sub(r'[^a-zA-Z0-9]', '', stringa_pulita)
    return stringa_pulita.lower()

def get_lyrics(artist, song_title):
    url = f"https://www.azlyrics.com/lyrics/{artist}/{song_title}.html"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        lyrics_div = soup.find_all("div", class_=None, id=None)[0]
        lyrics = lyrics_div.text.strip()
        return lyrics
    else:
        return "Lyrics not found."

for index, row in df_brani.iterrows():
    time.sleep(5) # 5 secondi
    artist = list(prolog.query(f"artista(\"{row['main_artist_id']}\", Nome)"))[0]['Nome'].decode("ASCII")
    print(artist)
    song_title = row['track_name']
    print(song_title)
    
    print(get_lyrics(rimuovi_simboli_speciali(artist), rimuovi_simboli_speciali(song_title)))