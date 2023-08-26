import os
import re
import pandas as pd
import numpy as np
import spotipy
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix, \
    RocCurveDisplay, PrecisionRecallDisplay
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import lyricsgenius as lg
from spotipy.oauth2 import SpotifyOAuth
from yellowbrick.model_selection import learning_curve

genius_id = "Oejkq5pM7oYgIfKI5IidSAe1qqsVCgLZ8DR4O-B3hMd3p-QNahQF79_SeFNHs09M"
genius_secret = "rWrWimfnUHCytx6e_xsEy_u6N2mBzpFp6vX-4ArQTp4Q5sUGKXNlnD2_kucXplneK5_-ozNiLjuinckCaNeBTg"
genius_access_token = "dichmTVxVdSkWt18dizB-Tia_pfS5TQC93qht-dOXLssAo5t786eeqUWfPDmEgtD"

client_id = "1572e8f11a55483ba6336cc98058160e"
client_secret = "f6e304f95c1d41d1b3f9434437e88435"
redirect_uri = "http://localhost:8888/callback"

print("Autenticazione Spotify in corso...")

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri=redirect_uri, scope='user-library-read')
sp = spotipy.Spotify(auth_manager=auth_manager)

print("Autenticazione Spotify eseguita con successo!")

print("Autenticazione Genius in corso...")

genius = lg.Genius(genius_access_token)
genius.timeout = 15  # 15 va bene
genius.sleep_time = 1
np.random.seed(5)

print("Autenticazione Genius eseguita con successo!")

path_brani_preferiti = "../datasets/brani_preferiti_2023-08-11.csv"
path_brani_scaricati = "../datasets/brani_scaricati_2023-08-11.csv"

dfBraniPreferiti = pd.read_csv(path_brani_preferiti)
dfBraniScaricati = pd.read_csv(path_brani_scaricati)

dfBraniPreferiti['Liked'] = 1
dfBraniScaricati['Liked'] = 0

dfCombinati = pd.merge(dfBraniPreferiti, dfBraniScaricati, how='outer')

def pulisciTesto(input_string):
    indiceTestoPulito = input_string.find('\n')
    input_string = input_string[indiceTestoPulito + 1:]

    pattern = r'\[.*?\]'  # Pattern per trovare le sottostringhe tra '[' e ']'
    input_string = re.sub(pattern, '', input_string)  # Sostituisci le sottostringhe con una stringa vuota
    return input_string