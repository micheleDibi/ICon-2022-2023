# Salvataggio Brani
L’obbiettivo è quello di salvare in un file csv le canzoni presenti nei brani preferiti nell’account di @michele dibisceglia. Innanzitutto sono stati recuperati dalla piattaforma spotify developer [https://developer.spotify.com/dashboard/1572e8f11a55483ba6336cc98058160e/settings](https://developer.spotify.com/dashboard/1572e8f11a55483ba6336cc98058160e/settings) `client_id`, `client_secret` e `redirect_uri` per poter effettuare la fase di autenticazione. Sono state create tre tabelle, collegate tra loro mediante gli id (come se fosse un database relazionale). rispettivamente, brani, artisti e album per una migliore organizzazione e congruenza dei dati. In una fase successiva del progetto, queste associazioni andranno fatte con Prolog. Utilizzando la funzione `current_user_saved_tracks()` e la funzione `audio_features(track_id)`, passandogli come parametro l’id di ogni brano, sono stati recuperati i seguenti dati:

- `track_id`: Spotify ID del brano;
- `track_added_at`: data e ora in cui il brano è stato salvato. Il timestamps è restituito in formato ISO 8601 come Coordinated Universal Time (UTC): YYYY-MM-DDTHH:MM:SSZ;
- `track_name`: nome del brano;
- `album_id`: album di appartenenza del brano;
- `main_artist_id`: artista principale del brano;
- `side_artists_id`: lista di artisti secondari che hanno partecipato nel brano;
- `track_duration`: durata in millisecondi del brano
- `track_explicit`: variabile booleana che indica se nel brano sono presenti riferimenti espliciti
- `track_popularity`: popolarità della traccia. Si tratta di un valore compreso tra 0 e 100, in cui 100 indica più popolare. La popolarità è calcolata tramite un algoritmo (interno di Spotify) ed è basato maggiormente, sul numero totale di riproduzioni del brano e su quanto sono recenti;
- `track_key`: La tonalità in cui si trova la traccia. Gli interi corrispondono alle tonalità utilizzando la notazione standard della Pitch Class. Ad esempio, 0 = C, 1 = C♯/D♭, 2 = D e così via. Se non è stata rilevata alcuna tonalità, il valore è -1.
- `track_bpm (*tempo*)`: Il tempo complessivo stimato di un brano in battiti al minuto (BPM). Nella terminologia musicale, il tempo è la velocità o il ritmo di un determinato brano e deriva direttamente dalla durata media dei battiti.
- `track_energy`: L'energia è una misura che va da 0,0 a 1,0 e rappresenta una misura percettiva dell'intensità e dell'attività. In genere, i brani energetici sono veloci, forti e rumorosi. Ad esempio, il death metal ha un'energia elevata, mentre un preludio di Bach ha un punteggio basso su questa scala. Le caratteristiche percettive che contribuiscono a questo attributo includono la gamma dinamica, il volume percepito, il timbro, la velocità di insorgenza e l'entropia generale.
- `track_danceability`: La ballabilità descrive quanto un brano sia adatto al ballo in base a una combinazione di elementi musicali, tra cui il tempo, la stabilità del ritmo, la forza del battito e la regolarità generale. Un valore di 0,0 è il meno ballabile e di 1,0 è il più ballabile.
- `track_happiness (*valence*)`: Una misura da 0,0 a 1,0 che descrive la positività musicale trasmessa da un brano. I brani con alta valenza suonano più positivi (ad esempio, felici, allegri, euforici), mentre quelli con bassa valenza suonano più negativi (ad esempio, tristi, depressi, arrabbiati).
- `track_loudness`: Il volume complessivo di una traccia in decibel (dB). I valori di loudness sono mediati sull'intero brano e sono utili per confrontare il volume relativo dei brani. Il loudness è la qualità di un suono che è il principale correlato psicologico della forza fisica (ampiezza). I valori sono tipicamente compresi tra -60 e 0 db.
- `track_acousticness`: Una misura di fiducia da 0,0 a 1,0 che indica se il brano è acustico. 1,0 rappresenta un'elevata fiducia che il brano sia acustico.
- `track_instrumentalness`: Prevede se un brano non contiene voci. I suoni "ooh" e "aah" sono considerati strumentali in questo contesto. I brani rap o parlati sono chiaramente "vocali". Più il valore di strumentalità è vicino a 1,0, maggiore è la probabilità che il brano non contenga contenuti vocali. I valori superiori a 0,5 sono intesi come tracce strumentali, ma la fiducia è maggiore man mano che il valore si avvicina a 1,0.
- `track_liveness`: Rileva la presenza di un pubblico nella registrazione. Valori di vivacità più alti rappresentano una maggiore probabilità che il brano sia stato eseguito dal vivo. Un valore superiore a 0,8 indica una forte probabilità che il brano sia dal vivo.
- `track_mode`: Il modo indica la modalità (maggiore o minore) di un brano, cioè il tipo di scala da cui deriva il suo contenuto melodico. Maggiore è rappresentato da 1 e minore da 0.
- `track_speechiness`: speechiness rileva la presenza di parole parlate in una traccia. Più la registrazione è esclusivamente di tipo parlato (ad esempio, talk show, audiolibri, poesie), più il valore dell'attributo è vicino a 1,0. I valori superiori a 0,66 descrivono tracce che probabilmente sono costituite interamente da parole parlate. I valori compresi tra 0,33 e 0,66 descrivono tracce che possono contenere sia musica che parlato, in sezioni o stratificati, compresi i casi di musica rap. I valori inferiori a 0,33 rappresentano molto probabilmente musica e altre tracce non simili al parlato.
- `track_time_signature`: Una firma temporale stimata. La firma temporale (metro) è una convenzione di notazione per specificare quante battute ci sono in ogni battuta (o misura). La firma temporale va da 3 a 7, indicando firme temporali da "3/4" a "7/4".

Una volta che sono stati recuperati tutti i brani preferiti, questi sono stati salvati nel file ******************saved_tracks_2023-07-22.csv******************

Per gli album invece, utilizzando la funzione `album(album_id)` sono stati recuperati i seguenti dati:

- `album_id`: ID Spotify dell’album
- `album_name`: nome dell’album
- `album_total_track`: numero di brano presenti nell’album
- `album_type`: tipo di album (sotto forma di stringa) i cui unici valori consentiti sono ‘*album*’, ‘*compilation*’ e ‘*single*’
- `album_label`: etichetta discografica che ha prodotto l’album
- `album_popularity`: popolarità dell’album. Il valore è compreso da 0 e 100 dove 100 indica maggiore popolarità.

Tra di dati che potevano essere recuperati tramite l’API era presente anche il campo `album_genres` il quale dovrebbe indicare il genere (o i generi) dell’album. Dopo una prima valutazione si è notato che questo campo facendo richiesta all’API viene sempre restituito vuoto, per questo motivo è stato omesso.

In ultimo, i dati degli artisti, recuperati utilizzando la funzione `artist(artist_id)` 

- `artist_id`: ID Spotify dell’artista
- `artist_name`: nome dell’artista
- `artist_followers`: numero di seguaci dell’artista
- `artist_genres`: generi musicali dell’artista
- `artist_popularity`: popolarità dell’artista. Il valore è compreso tra 0 e 100 dove 100 indica maggiore popolarità

Ciascuna delle tre tabelle, dopo aver eliminato eventuali righe duplicate, sono state salvate in file csv.
