import spotipy
import pyswip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score, KFold


client_id = "1572e8f11a55483ba6336cc98058160e"
client_secret = "f6e304f95c1d41d1b3f9434437e88435"
redirect_uri = "http://localhost:8888/callback"

tree_depth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

print("Autenticazione Spotify in corso...")
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri=redirect_uri, scope='user-library-read')
print("Autenticazione Spotify eseguita con successo!")
sp = spotipy.Spotify(auth_manager=auth_manager)
"""
# Per ottenere solo i primi 20 risultati
results = sp.current_user_saved_tracks(limit=20)
brani_preferiti = results['items']
"""
print("Inizio di recupero brani preferiti...")
# Per ottenere tutti i brani preferiti
offset = 0
limit = 50  # Numero massimo di brani che possono essere recuperati in una chiamata all'API
brani_preferiti = []

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    tracks = results['items']

    if not tracks:
        break

    brani_preferiti.extend(tracks)
    offset += limit
print("Brani preferiti recuperati con successo!")
prolog = pyswip.Prolog()
brani = []

prolog.assertz("use_module(library(datetime))")


def escape_string(string):
    return string.replace("'", '_').replace(' ', '_')


def save_track(brano):
    info_brano = brano['track']
    print(f"Salvataggio brano {info_brano['name']} ...")
    features = sp.audio_features(info_brano['id'])

    collaboratori = []
    for collaboratore in info_brano['artists'][1:]:
        collaboratori.append(escape_string(collaboratore['name']))

    if features[0] != None:
        key = features[0]['key']
        bpm = round(features[0]['tempo'])
        energy = round(features[0]['energy'], 2)
        danceability = round(features[0]['danceability'], 2)
        happiness = round(features[0]['valence'], 2)
        loudness = round(features[0]['loudness'], 2)
        acousticness = round(features[0]['acousticness'], 2)
        instrumentalness = round(features[0]['instrumentalness'], 3)
        liveness = round(features[0]['liveness'], 2)
        mode = features[0]['mode']
        speechiness = round(features[0]['speechiness'], 3)
        time_signature = features[0]['time_signature']
        valence = features[0]['valence']
    else:
        key = 'null'
        bpm = 'null'
        energy = 'null'
        danceability = 'null'
        happiness = 'null'
        loudness = 'null'
        acousticness = 'null'
        instrumentalness = 'null'
        liveness = 'null'
        mode = 'null'
        speechiness = 'null'
        time_signature = 'null'
        valence = 'null'

    brano_corrente = {
        'id': info_brano['id'],
        'name': escape_string(info_brano['name']),
        'album': escape_string(info_brano['album']['name']),
        'uscita': info_brano['album']['release_date'],
        'artista': escape_string(info_brano['artists'][0]['name']),
        'collaboratori': collaboratori,
        'generi': sp.artist(info_brano['artists'][0]['id'])['genres'],
        'popularity': info_brano['popularity'],
        'key': key,
        'bpm': bpm,
        'energy': energy,
        'danceability': danceability,
        'happiness': happiness,
        'loudness': loudness,
        'acousticness': acousticness,
        'instrumentalness': instrumentalness,
        'liveness': liveness,
        'mode': mode,
        'speechiness': speechiness,
        'time_signature': time_signature,
        'valence': valence

    }

    print(f"Salvataggio brano {info_brano['name']} eseguito con successo!")
    print(f"Asserzioni Prolog {info_brano['name']} ...")

    prolog.assertz(f"canzone('{brano_corrente['name']}')")
    prolog.assertz(f"album('{brano_corrente['album']}')")
    prolog.assertz(f"dataUscita('{brano_corrente['album']}', '{brano_corrente['uscita']}')")
    prolog.assertz(f"artista('{brano_corrente['artista']}')")
    prolog.assertz(f"haCreato('{brano_corrente['artista']}', '{brano_corrente['album']}')")
    prolog.assertz(f"appartieneA('{brano_corrente['name']}', '{brano_corrente['album']}')")

    for genere in brano_corrente['generi']:
        prolog.assertz(f"genere('{brano_corrente['name']}', '{escape_string(genere)}')")

    for collaboratore in brano_corrente['collaboratori']:
        prolog.assertz(
            f"haCollaborato('{brano_corrente['artista']}', '{escape_string(collaboratore)}', '{brano_corrente['name']}')")

    prolog.assertz(f"popolarita('{brano_corrente['name']}', '{brano_corrente['popularity']}')")

    prolog.assertz(f"attributo('{brano_corrente['name']}', tonalita,'{brano_corrente['key']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', bpm,'{brano_corrente['bpm']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', energy,'{brano_corrente['energy']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', danceability,'{brano_corrente['danceability']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', happiness,'{brano_corrente['happiness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', loudness,'{brano_corrente['loudness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', acousticness,'{brano_corrente['acousticness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', instrumentalness,'{brano_corrente['instrumentalness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', liveness,'{brano_corrente['liveness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', mode,'{brano_corrente['mode']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', speechiness,'{brano_corrente['speechiness']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', time_signature,'{brano_corrente['time_signature']}')")
    prolog.assertz(f"attributo('{brano_corrente['name']}', valence,'{brano_corrente['valence']}')")

    print(f"Asserzioni Prolog {info_brano['name']} completate con successo!")

    return brano_corrente


for brano in brani_preferiti:
    brani.append(save_track(brano))

df_brani_preferiti = pd.DataFrame(brani)

print("Selezione dei 10 artisti più presenti nei brani preferiti... ")
# Selezione dei 10 artisti più presenti nei brani preferiti
artist_freq = df_brani_preferiti['artista'].value_counts()
top_10_artisti = artist_freq.head(10).index.tolist()
for artista in top_10_artisti:
    print(artista)
    prolog.assertz(f"haApprezzatoParticolarmente('utente1', '{artista}')")
print("Fine dei 10 artisti più presenti")

print("Selezione dei 10 generi più presenti nei brani preferiti...")
# Selezione dei 10 generi più presenti nei brani preferiti
all_genres = [genre for genres in df_brani_preferiti['generi'] for genre in genres]
genres_freq = pd.Series(all_genres).value_counts()
top_10_generi = genres_freq.head(10).index.tolist()
for genere in top_10_generi:
    print(genere)
    prolog.assertz(f"haAscoltatoFrequentemente('utente1', '{escape_string(genere)}')")
print("Fine dei 10 generi più presenti")

print("Inizio raccolta dei brani presenti nella playlist 'New Music Friday'...")
# ID Playlist 'New Music Friday'
playlist_ID = "37i9dQZF1DX4JAvHpjipBk"
results = sp.playlist(playlist_id=playlist_ID)
new_music_friday = []

tracks = results['tracks']['items']
for track in tracks:
    new_music_friday.append(save_track(track))

df_new_music_friday = pd.DataFrame(new_music_friday)
print("Raccolta dei brani presenti nella playlist 'New Music Friday' eseguita con successo!")

print("Inizio raccolta dei brani presenti nella playlist 'New Music Friday Italy'...")
# ID Playlist 'New Music Friday Italy'
playlist_ID = "37i9dQZF1DWVKDF4ycOESi"
results = sp.playlist(playlist_id=playlist_ID)
new_music_friday_italy = []

tracks = results['tracks']['items']
for track in tracks:
    new_music_friday_italy.append(save_track(track))

df_new_music_friday_italy = pd.DataFrame(new_music_friday_italy)

print("Raccolta dei brani presenti nella playlist 'New Music Friday Italy' eseguita con successo!")

print("Inizio raccolta dei brani presenti nella playlist 'Top 50 Italia'...")

# ID Playlist 'Top 50 Italia'
playlist_ID = "37i9dQZEVXbIQnj7RRhdSX"
results = sp.playlist(playlist_id=playlist_ID)
top_50_italia = []

tracks = results['tracks']['items']
for track in tracks:
    top_50_italia.append(save_track(track))

df_top_50_italia = pd.DataFrame(top_50_italia)
print("Raccolta dei brani presenti nella playlist 'Top 50 Italia' eseguita con successo!")

print("Inizio raccolta dei brani presenti nella playlist 'in tendenza'...")

# ID Playlist 'Hot Hits Italia'
playlist_ID = "37i9dQZF1DX6wfQutivYYr"
results = sp.playlist(playlist_id=playlist_ID)
in_tendenza = []

tracks = results['tracks']['items']
for track in tracks:
    in_tendenza.append(save_track(track))

df_in_tendenza = pd.DataFrame(in_tendenza)
print("Raccolta dei brani presenti nella playlist 'in tendenza' eseguita con successo!")

"""Se una canzone "X" appartiene all'album "Y" e l'album "Y" è stato creato dall'artista "Z", allora la canzone "X" 
appartiene all'artista "Z";"""
prolog.assertz("appartieneAllArtista(C, A) :- appartieneA(C, E), haCreato(A, E)")

"""Se una canzone 'X' condivide un alto numero di attributi musicali, come il genere, il ritmo e la tonalità, 
con una canzone 'Y', allora la canzone 'X' è considerata simile alla canzone 'Y'"""
prolog.assertz("attributo_comune(X, Y, Attributo) :- attributo(X, Attributo, Valore), attributo(Y, Attributo, Valore)")
prolog.assertz("numero_attributi_comuni(X, Y, NumeroAttributi) :- setof(Attributo, attributo_comune(X, Y, Attributo), "
               "AttributiComuni), length(AttributiComuni, NumeroAttributi)")
prolog.assertz("hannoGenereComune(X, Y) :- genere(X, Genere), genere(Y, Genere), X \= Y")
prolog.assertz("simili(X, Y) :- numero_attributi_comuni(X, Y, NumeroAttributi), NumeroAttributi > 7, "
               "hannoGenereComune(X, Y)")

"""Se un utente 'A' ha ascoltato frequentemente canzoni di un genere 'X' e ha apprezzato particolarmente le canzoni 
dell'artista 'Y', allora è probabile che l'utente 'A' gradisca anche altre canzoni dello stesso genere o dell'artista 
'Y'"""
prolog.assertz("gradisceCanzoneGenere(A, Canzone) :- haAscoltatoFrequentemente(A, GenereX),  genere(Canzone, GenereX)")
prolog.assertz(
    "gradisceCanzoneArtista(A, Canzone) :- haApprezzatoParticolarmente(A, ArtistaY), haCreato(ArtistaY, Album), "
    "appartieneA(Canzone, Album)")

"""Se un artista 'X' ha collaborato con un artista 'Y' in passato per creare una canzone 'Z' e l'artista 'Y' ha 
successivamente creato un nuovo album 'W', allora l'artista 'X' potrebbe essere coinvolto anche nell'album 'W'"""
prolog.assertz("coinvolto(ArtistaX, AlbumW) :- haCollaborato(ArtistaX, ArtistaY, CanzoneZ), haCreato(ArtistaY, AlbumW),"
               "appartieneA(CanzoneZ, AlbumZ), dataUscita(AlbumZ, DataUscitaZ), dataUscita(AlbumW, DataUscitaW), DataUscitaW @> DataUscitaZ")


def ragionamento_dataframe(df):
    for index, row in df.iterrows():
        nome_brano = row['name']
        nome_album = row['album']

        # appartieneAllArtista - la canzone è di uno degli artisti preferiti dell'utente
        results_query = bool(list(prolog.query(f"appartieneAllArtista('{nome_brano}', Artista), "
                                               f"haApprezzatoParticolarmente('utente1', Artista)")))

        if results_query:
            df.at[index, 'canzoneArtistaPreferito'] = 1
        else:
            df.at[index, 'canzoneArtistaPreferito'] = 0

        # simili - canzone simile di un artista che gli piace
        results_query = bool(list(prolog.query(f"simili('{nome_brano}', Canzone), appartieneAllArtista(Canzone, "
                                               "Artista), haApprezzatoParticolarmente('utente1', Artista)")))

        if results_query:
            df.at[index, 'canzoneSimileArtistaPreferito'] = 1
        else:
            df.at[index, 'canzoneSimileArtistaPreferito'] = 0

        # simili - canzone simile di un genere che gli piace
        results_query = bool(list(prolog.query(f"simili('{nome_brano}', Canzone),  gradisceCanzoneGenere(A, Canzone)")))

        if results_query:
            df.at[index, 'canzoneSimileGenerePreferito'] = 1
        else:
            df.at[index, 'canzoneSimileGenerePreferito'] = 0

        # genereGradito
        results_query = bool(list(prolog.query(f"gradisceCanzoneGenere(A, '{nome_brano}')")))

        if results_query:
            df.at[index, 'GenerePreferito'] = 1
        else:
            df.at[index, 'GenerePreferito'] = 0

        # artistaGradito
        results_query = bool(list(prolog.query(f"gradisceCanzoneArtista(A, '{nome_brano}')")))

        if results_query:
            df.at[index, 'artistaPreferito'] = 1
        else:
            df.at[index, 'artistaPreferito'] = 0

        # artistaPreferitoGradito - coinvolto
        results_query = bool(list(
            prolog.query(f"coinvolto(ArtistaX, '{nome_album}'), haApprezzatoParticolarmente('utente1', ArtistaX)")))

        if results_query:
            df.at[index, 'artistaPreferitoCoinvolto'] = 1
        else:
            df.at[index, 'artistaPreferitoCoinvolto'] = 0

    return df


df_brani_preferiti = ragionamento_dataframe(df_brani_preferiti)
df_brani_preferiti.to_csv("brani_preferiti.csv", index=False)

df_in_tendenza = ragionamento_dataframe(df_in_tendenza)
df_in_tendenza.to_csv(f"in_tendenza_{date.today()}.csv", index=False)

df_top_50_italia = ragionamento_dataframe(df_top_50_italia)
df_top_50_italia.to_csv(f"top_50_italia_{date.today()}.csv", index=False)

df_new_music_friday = ragionamento_dataframe(df_new_music_friday)
df_new_music_friday.to_csv(f"new_music_friday_{date.today()}.csv", index=False)

df_new_music_friday_italy = ragionamento_dataframe(df_new_music_friday_italy)
df_new_music_friday_italy.to_csv(f"new_music_friday_italy_{date.today()}.csv", index=False)

print("Inizio concatenazione dei vari dataset... ")
df_dataset = pd.concat([df_top_50_italia, df_in_tendenza, df_new_music_friday_italy, df_new_music_friday],
                       ignore_index=True)

df_dataset['preferito'] = 0
df_brani_preferiti['preferito'] = 1

df_combined = pd.concat([df_dataset, df_brani_preferiti], ignore_index=True)

print("Concatenazione dei vari dataset eseguita con successo!")
print("Inizio operazioni per l'addestramento dei modelli di apprendimento...")

selected_columns = ["bpm", "popularity", "energy", "danceability", "happiness", "loudness", "acousticness",
                    "canzoneArtistaPreferito", "canzoneSimileArtistaPreferito", "canzoneSimileGenerePreferito",
                    "GenerePreferito", "artistaPreferitoCoinvolto", "instrumentalness", "liveness", "mode",
                    "speechiness", "time_signature", "valence"]

X = df_combined[selected_columns]
y = df_combined['preferito']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = [
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    GradientBoostingClassifier(),
    KNeighborsClassifier()
]
print("Operazioni per l'addestramento dei modelli di apprendimento completate con successo!")
print("Inizio operazioni di apprendimento e previsione...")


# Decision Tree Classifier
def trainingAndTestScoresDTC(X: pd.DataFrame, y: pd.Series):
    train_score_mean = []
    test_score_mean = []
    precision_mean = []
    recall_mean = []
    f1_mean = []

    for i in range(1, 16):
        classifier = DecisionTreeClassifier(max_depth=i, criterion="entropy")

        kfold = KFold(n_splits=10, shuffle=True, random_state=42)

        scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        results = cross_validate(classifier, X, y, cv=kfold, scoring=scoring, return_train_score=True)

        train_accuracy_scores = results['train_accuracy']
        test_accuracy_scores = results['test_accuracy']

        precision_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='precision_macro')
        recall_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='recall_macro')
        f1_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='f1_macro')

        train_score_mean.append(np.average(train_accuracy_scores))
        test_score_mean.append(np.average(test_accuracy_scores))

        precision_mean.append(precision_scores.mean())
        recall_mean.append(recall_scores.mean())
        f1_mean.append(f1_scores.mean())

    return train_score_mean, test_score_mean, np.average(precision_mean), np.average(recall_mean), np.average(f1_mean)


DTCtrainingScores, DTCtestScores, p, r, f = trainingAndTestScoresDTC(X, y)
print("Training and test scores Decision Tree Classifier")
print(f"Training Scores: {DTCtrainingScores}")
print(f"Test Scores: {DTCtestScores}")
print(f"Precision: {p}")
print(f"Recall: {r}")
print(f"F1 Measure: {f}")

plt.figure(figsize=(10, 10))
plt.plot(tree_depth, DTCtrainingScores, marker='o', linestyle='-', color='b', label='Training Scores')
plt.plot(tree_depth, DTCtestScores, marker='o', linestyle='-', color='r', label='Test Scores')
plt.xlabel("Profondità degli alberi")
plt.ylabel('Scores')
plt.title("Prestazioni del modello 'Decision Tree Classifier' in base alla profondità degli alberi")
plt.legend(loc='lower right')

plt.savefig('DecisionTreeClassifier.png')


# Random Forest Classifier
def trainingAndTestScoresRFC(X: pd.DataFrame, y: pd.Series):
    train_score_mean = []
    test_score_mean = []
    precision_mean = []
    recall_mean = []
    f1_mean = []

    for i in range(1, 16):
        classifier = RandomForestClassifier(max_depth=i, criterion="entropy")

        kfold = KFold(n_splits=10, shuffle=True, random_state=42)

        scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        results = cross_validate(classifier, X, y, cv=kfold, scoring=scoring, return_train_score=True)

        train_accuracy_scores = results['train_accuracy']
        test_accuracy_scores = results['test_accuracy']

        precision_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='precision_macro')
        recall_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='recall_macro')
        f1_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='f1_macro')

        train_score_mean.append(np.average(train_accuracy_scores))
        test_score_mean.append(np.average(test_accuracy_scores))

        precision_mean.append(precision_scores.mean())
        recall_mean.append(recall_scores.mean())
        f1_mean.append(f1_scores.mean())

    return train_score_mean, test_score_mean, np.average(precision_mean), np.average(recall_mean), np.average(f1_mean)


RFCtrainingScores, RFCtestScores, p, r, f = trainingAndTestScoresRFC(X, y)
print("Training and test scores Random Forest Classifier")
print(f"Training Scores: {RFCtrainingScores}")
print(f"Test Scores: {RFCtestScores}")
print(f"Precision: {p}")
print(f"Recall: {r}")
print(f"F1 Measure: {f}")

plt.figure(figsize=(10, 10))
plt.plot(tree_depth, RFCtrainingScores, marker='o', linestyle='-', color='b', label='Training Scores')
plt.plot(tree_depth, RFCtestScores, marker='o', linestyle='-', color='r', label='Test Scores')
plt.xlabel("Profondità degli alberi")
plt.ylabel('Scores')
plt.title("Prestazioni del modello 'Random Forest Classifier' in base alla profondità degli alberi")
plt.legend(loc='lower right')

plt.savefig('RandomForestClassifier.png')

# Gradient Boosting Classifier
def trainingAndTestScoresGBC(X: pd.DataFrame, y: pd.Series):
    train_score_mean = []
    test_score_mean = []
    precision_mean = []
    recall_mean = []
    f1_mean = []

    for i in range(10, 151, 10):
        classifier = GradientBoostingClassifier(n_estimators=i)

        kfold = KFold(n_splits=10, shuffle=True, random_state=42)

        scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
        results = cross_validate(classifier, X, y, cv=kfold, scoring=scoring, return_train_score=True)

        train_accuracy_scores = results['train_accuracy']
        test_accuracy_scores = results['test_accuracy']

        precision_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='precision_macro')
        recall_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='recall_macro')
        f1_scores = cross_val_score(classifier, X, y, cv=kfold, scoring='f1_macro')

        train_score_mean.append(np.average(train_accuracy_scores))
        test_score_mean.append(np.average(test_accuracy_scores))

        precision_mean.append(precision_scores.mean())
        recall_mean.append(recall_scores.mean())
        f1_mean.append(f1_scores.mean())

    return train_score_mean, test_score_mean, np.average(precision_mean), np.average(recall_mean), np.average(f1_mean)


GBCtrainingScores, GBCtestScores, p, r, f = trainingAndTestScoresGBC(X, y)
print("Training and test scores Gradient Boosting Classifier")
print(f"Training Scores: {GBCtrainingScores}")
print(f"Test Scores: {GBCtestScores}")
print(f"Precision: {p}")
print(f"Recall: {r}")
print(f"F1 Measure: {f}")

plt.figure(figsize=(10, 10))
plt.plot(tree_depth, GBCtrainingScores, marker='o', linestyle='-', color='b', label='Training Scores')
plt.plot(tree_depth, GBCtestScores, marker='o', linestyle='-', color='r', label='Test Scores')
plt.xlabel("Profondità degli alberi")
plt.ylabel('Scores')
plt.title("Prestazioni del modello 'Gradient Boosting Classifier' in base alla profondità degli alberi")
plt.legend(loc='lower right')

plt.savefig('GradientBoostingClassifier.png')


def trainingAndTestScoresKNN(X_train, y_train, X_test, y_test):
    trainingScores = []
    testScores = []

    k = 1
    max_k = 20

    while k <= max_k:
        tree = KNeighborsClassifier(n_neighbors=k)
        tree.fit(X_train, y_train)

        trainingScores.append(tree.score(X_train, y_train))
        testScores.append(tree.score(X_test, y_test))

        k += 1

    return trainingScores, testScores


KNNtrainingScores, KNNtestScores = trainingAndTestScoresKNN(X_train, y_train, X_test, y_test)
print("Training and test scores KNN")
print(KNNtrainingScores)
print(KNNtestScores)

k = 1
max_k = 20

knn = []

while k <= max_k:
    knn.append(k)
    k += 1

plt.figure(figsize=(10, 10))
plt.plot(knn, KNNtrainingScores, marker='o', linestyle='-', color='b', label='Training Scores')
plt.plot(knn, KNNtestScores, marker='o', linestyle='-', color='r', label='Test Scores')
plt.xlabel("N-Neighbours")
plt.ylabel('Scores')
plt.title("Prestazioni del modello 'KNN' in base alla profondità degli alberi")
plt.legend(loc='lower right')

plt.savefig('KNN.png')

for model in models:
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    print(classification_report(y_test, prediction))

    # Creazione di file contenenti i brani consigliati in ordine
    df_altre_canzoni = pd.concat([df_top_50_italia, df_in_tendenza, df_new_music_friday_italy, df_new_music_friday],
                                 ignore_index=True)
    X_other_songs = df_altre_canzoni[selected_columns]
    prediction = model.predict(X_other_songs)
    df_altre_canzoni['prediction'] = prediction
    canzoni_possibili = df_altre_canzoni[df_altre_canzoni['prediction'] == 1]
    canzoni_possibili.to_csv(f"canzoni_possibili_{type(model).__name__}.csv", index=True)

print("Fine operazioni di apprendimento e previsione! Controlla i risultati!")

print("Inizio apprendimento non supervisionato...")

features = ['key', 'bpm', 'energy', 'danceability', 'happiness', 'loudness', 'acousticness', "instrumentalness",
            "liveness", "mode", "speechiness", "time_signature", "valence"]

data = df_brani_preferiti[features]

k = 30
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(data)

# Visualizzazione dei cluster
pca = PCA(n_components=2)
data_transformed = pca.fit_transform(data)

plt.figure(figsize=(10, 10))
plt.scatter(data_transformed[:, 0], data_transformed[:, 1], c=kmeans.labels_)
plt.xlabel("Componente Principale 1")
plt.ylabel("Componente Principale 2")
plt.title("Visualizzazione dei Cluster")
plt.savefig("canzoni_anomale.png")

# Calcolo della frequenza dei cluster
df_brani_preferiti['cluster_labels'] = kmeans.labels_
cluster_frequencies = df_brani_preferiti['cluster_labels'].value_counts()

min_frequency = cluster_frequencies.min()

anomalous_cluster = cluster_frequencies[cluster_frequencies == min_frequency].index

anomalous_songs = df_brani_preferiti[df_brani_preferiti['cluster_labels'].isin(anomalous_cluster)]
# Identifica i cluster meno frequenti rispetto agli altri
# anomalous_cluster = cluster_frequencies[cluster_frequencies < cluster_frequencies.mean()].index

# Identifica le canzoni che si discostano dagli ascolti tipici
# anomalous_songs = df_brani_preferiti[df_brani_preferiti['cluster_labels'].isin(anomalous_cluster)]

print("Canzoni anomale: ")
print(anomalous_songs[['name', 'artista']])

anomalous_songs.to_csv("canzoni_anomale.csv")

print("Apprendimento non supervisionato completato con successo!")
