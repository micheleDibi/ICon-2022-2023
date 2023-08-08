import pandas as pd
from os.path import exists

import seaborn as sns
from sklearn.preprocessing import StandardScaler
from datetime import date
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

path_favorites_tracks = "brani_preferiti_2023-08-06.csv"
path_saved_tracks = "brani_scaricati_2023-08-06.csv"

if exists(path_saved_tracks) and exists(path_favorites_tracks):
    df_favorites_tracks = pd.read_csv(path_favorites_tracks)
    df_saved_tracks = pd.read_csv(path_saved_tracks)
    df_favorites_tracks["liked"] = True
    df_saved_tracks["liked"] = False
    df_tracks = pd.concat([df_favorites_tracks, df_saved_tracks])
    
    # print(df_favorites_tracks.info())
    # print(df_saved_tracks.info())
    # print(df_tracks.info())
    
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

    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df_tracks[columns_to_scale])
    scaled_dataframe = pd.DataFrame(scaled_array, columns=columns_to_scale)
    
    df_tracks[columns_to_scale] = scaled_array
        
    plt.figure(figsize=(15, 6))
    sns.heatmap(scaled_dataframe.corr(), annot=True)
    plt.show()
    
    plt.figure(figsize=(15, 6))
    sns.boxplot(data = scaled_dataframe, orient="h")
    plt.show()
    
    plt.figure(figsize=(15, 6))
    sns.pairplot(scaled_dataframe)
    plt.show()
    
    plt.figure(figsize=(15, 6))
    sns.boxplot(data = scaled_dataframe, orient="h")
    plt.show()
    
    # print(scaled_dataframe.describe())
    
    kmeans_model = KMeans(n_clusters=15, n_init=10, init='k-means++')
    kmeans_model.fit(df_tracks[columns_to_scale])
    # kmeans_model.fit(df_tracks[['track_bpm', 'track_time_signature', 'track_key']])
    
    centroids = kmeans_model.cluster_centers_
    
    df_tracks["cluster"] = kmeans_model.labels_
    print(df_tracks["cluster"].value_counts()) 

    df_tracks.to_csv(f"scaled_dataframe_clustering_{date.today()}.csv")
    
    # plt.figure(figsize=(10, 8))
    # sns.scatterplot(data=scaled_dataframe, x='track_bpm', y='track_energy', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_danceability', y='track_happiness', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_loudness', y='track_acousticness', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_instrumentalness', y='track_speechiness', hue='cluster', palette='Set1')

    # plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=100)
    # plt.show()
    
    """
    k_values = range(2, 101)
    
    elbow_scores = []
    silhouette_scores = []
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, n_init='auto')
        kmeans.fit(df_tracks[columns_to_scale])
        
        elbow_scores.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(df_tracks[columns_to_scale], kmeans.labels_))
        
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, elbow_scores, marker='o')
    plt.xlabel("Numero di cluster (K)")
    plt.ylabel("Somma dei quadrati delle distanze")
    plt.title("Analisi del gomito")
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, silhouette_scores, marker='o')
    plt.xlabel("Numero di cluster (k)")
    plt.ylabel("Coef. di silhouette")
    plt.title("Coefficienti di silhouette")
    plt.show()
    """
else: print("Non è stato possibile trovare il file descritto, ricontrolla il path")