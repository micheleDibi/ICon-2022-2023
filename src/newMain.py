import pandas as pd
from os.path import exists

import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import date
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

import ast

from mapping_genres import map_genre_to_macro_category

path_favorites_tracks = "./datasets/brani_preferiti_2023-08-06.csv"
path_saved_tracks = "./datasets/brani_scaricati_2023-08-06.csv"
path_artists = "./datasets/artists_2023-08-06.csv"

def best_k_clustering(dataframe, min_value = 2, max_value = 11):
    k_values = range(min_value, max_value)
    
    elbow_scores = []
    silhouette_scores = []
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, n_init='auto')
        kmeans.fit(dataframe)
        
        elbow_scores.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(dataframe, kmeans.labels_))
        
    print(elbow_scores)        
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, elbow_scores, marker='o')
    plt.xlabel("Numero di cluster (K)")
    plt.ylabel("Somma dei quadrati delle distanze")
    plt.title("Analisi del gomito")
    plt.savefig("./img/analisi_del_gomito.png")
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, silhouette_scores, marker='o')
    plt.xlabel("Numero di cluster (k)")
    plt.ylabel("Coef. di silhouette")
    plt.title("Coefficienti di silhouette")
    plt.savefig("./img/coeff_silhouette.png")
    
def clustering(dataframe, columns, k):
    kmeans_model = KMeans(n_clusters=k, n_init=10, init='k-means++')
    kmeans_model.fit(dataframe[columns])
    
    # centroids = kmeans_model.cluster_centers_
    
    dataframe["cluster"] = kmeans_model.labels_
    print(dataframe["cluster"].value_counts()) 

    dataframe.to_csv(f"scaled_dataframe_clustering_{date.today()}.csv")
    

if exists(path_saved_tracks) and exists(path_favorites_tracks) and exists(path_artists):
    """
    df_favorites_tracks = pd.read_csv(path_favorites_tracks)
    df_saved_tracks = pd.read_csv(path_saved_tracks)
    df_favorites_tracks["liked"] = True
    df_saved_tracks["liked"] = False
    df_tracks = pd.concat([df_favorites_tracks, df_saved_tracks])
    """
    
    df_artists = pd.read_csv(path_artists)
    df_artists['artist_genres'] = df_artists['artist_genres'].apply(ast.literal_eval)   # trasforma le concatenazioni dei generi musicali in una lista di stringhe dei generi
    # df_artists = df_artists[df_artists['artist_genres'].apply(len) > 0]                 # elimina quegli artisti per cui non è stato definito il genere musicale
      
    # ogni categoria viene smistata in una macro categoria
    for index, row in df_artists.iterrows():
        macro_genres = []
    
        for genre in row['artist_genres']:
            macro_genres.append(map_genre_to_macro_category(genre))
    
        df_artists.at[index, 'artist_genres'] = macro_genres
    
    mlb = MultiLabelBinarizer()
    genre_encoded = mlb.fit_transform(df_artists['artist_genres'])
    genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_)
    df_encoded = pd.concat([df_artists.drop('artist_genres', axis=1), genre_df], axis=1)
    
    genre_columns = df_encoded.columns[5:]
    sum_of_genres = df_encoded[genre_columns].sum(axis=1)
    df_filtered = df_encoded[sum_of_genres > 0]
    
    columns_to_drop = [
        "artist_id",
        "artist_name",
        "artist_followers",
        "artist_popularity"
    ]
    
    df_filtered.to_csv("temp.csv")
            
    # best_k_clustering(dataframe=df_filtered.drop(columns=columns_to_drop), max_value=101)
    
    columns = list(df_filtered.columns)
    for column in columns_to_drop:
        columns.remove(column)
        
    clustering(df_filtered, columns, k = 10)

    """
    columns_to_scale = [
        'track_bpm',
        'track_energy',
        'track_danceability',
        'track_happiness',
        'track_loudness',
        'track_acousticness',
        'track_instrumentalness',
        'track_liveness',
        'track_speechiness'
    ]
    
    clustering_columns = [
        # 'track_bpm',
        # 'track_duration',
        'track_key',
        'track_mode',
        'track_time_signature'
        
        # 'track_energy',
        # 'track_danceability',
        # 'track_happiness',
        # 'track_loudness',
        # 'track_acousticness',
        # 'track_instrumentalness',
        # 'track_liveness',
        # 'track_speechiness',
    ]

    # print(df_tracks[columns_to_scale].describe())

    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df_tracks[columns_to_scale])
    scaled_dataframe = pd.DataFrame(scaled_array, columns=columns_to_scale)
    
    plt.figure(figsize=(15, 6))
    sns.heatmap(df_tracks[columns_to_scale].corr(), annot=True)
    plt.savefig("./img/heatmap.png")
    
    plt.figure(figsize=(15, 6))
    sns.boxplot(df_tracks[columns_to_scale], orient="h")
    plt.savefig("./img/boxplot_before_scaling.png")
    
    plt.figure(figsize=(15, 6))
    sns.boxplot(scaled_dataframe, orient="h")
    plt.savefig("./img/boxplot_after_scaling.png")
    
    # print(scaled_dataframe.describe())
    """
    
    # df_tracks[columns_to_scale] = scaled_array
    
    # best_k_clustering(df_tracks[clustering_columns])
    
else: print("Non è stato possibile trovare il file descritto, ricontrolla il path")