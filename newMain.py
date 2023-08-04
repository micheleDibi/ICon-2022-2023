import pandas as pd
from os.path import exists

import seaborn as sns
from sklearn.preprocessing import StandardScaler
from datetime import date
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

path_saved_tracks = "saved_tracks_2023-07-30.csv"

if exists(path_saved_tracks):
    df_saved_tracks = pd.read_csv(path_saved_tracks)
    
    print(df_saved_tracks.info())
        
    df_saved_tracks = df_saved_tracks[[
        'track_bpm',
        'track_energy',
        'track_danceability',
        'track_happiness',
        'track_loudness',
        'track_acousticness',
        'track_instrumentalness',
        'track_liveness',
        'track_speechiness'
    ]]
    
    # print(df_saved_tracks.info())
    
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df_saved_tracks)
    scaled_dataframe = pd.DataFrame(scaled_array, columns=df_saved_tracks.columns)
        
    # plt.figure(figsize=(15, 6))
    
    # sns.heatmap(df_saved_tracks.corr(), annot=True)
    # sns.boxplot(data = df_saved_tracks, orient="h")
    # sns.pairplot(scaled_dataframe)
    # sns.boxplot(data = scaled_dataframe, orient="h")
    # plt.show()
    
    # print(scaled_dataframe.describe())
    
    kmeans_model = KMeans(n_clusters=3, n_init=10, init='k-means++')
    kmeans_model.fit(scaled_dataframe)
    
    centroids = kmeans_model.cluster_centers_
    
    scaled_dataframe["cluster"] = kmeans_model.labels_
    # print(scaled_dataframe["cluster"].value_counts()) 

    scaled_dataframe.to_csv(f"scaled_dataframe_clustering_{date.today()}.csv")
    
    # plt.figure(figsize=(10, 8))
    # sns.scatterplot(data=scaled_dataframe, x='track_bpm', y='track_energy', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_danceability', y='track_happiness', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_loudness', y='track_acousticness', hue='cluster', palette='Set1')
    # sns.scatterplot(data=scaled_dataframe, x='track_instrumentalness', y='track_speechiness', hue='cluster', palette='Set1')

    # plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=100)
    # plt.show()
    
    """
    k_values = range(2, 16)
    
    elbow_scores = []
    silhouette_scores = []
    
    for k in k_values:
        kmeans = KMeans(init='k-means++', n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_dataframe)
        
        elbow_scores.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(df_saved_tracks, kmeans.labels_))
        
    print(elbow_scores)

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