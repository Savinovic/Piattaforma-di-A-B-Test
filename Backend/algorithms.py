import random
import pandas as pd
from flask import request, jsonify
from utils import load_ratings, load_links, merge_data, load_movies

from settings import RATINGS_FILE_PATH, LINKS_FILE_PATH, MOVIE_FILE_PATH, TAGS_FILE_PATH



def get_most_watched():
    from services import generate_recommendations

    # Carica i dati dai file CSV
    movies_df = load_movies(MOVIE_FILE_PATH)  # Contiene movieId, title, genres
    ratings_df = load_ratings(RATINGS_FILE_PATH)  # Contiene userId, movieId, rating, timestamp
    links_df = load_links(LINKS_FILE_PATH)  # Contiene movieId, imdbId, tmdbId
    
        # Conta il numero di valutazioni per ciascun film
    most_watched = ratings_df.groupby('movieId').size().reset_index(name='num_ratings')

    # Calcola la media delle valutazioni per ciascun film
    avg_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index(name='avg_rating')

    # Unisci il conteggio delle valutazioni con la media delle valutazioni
    most_watched = pd.merge(most_watched, avg_ratings, on='movieId')

    # Unisci con il dataframe dei film per ottenere i dettagli del film
    most_watched = merge_data(most_watched, movies_df)

    # Unisci con il dataframe dei link (per aggiungere IMDb e TMDb ID)
    most_watched = merge_data(most_watched, links_df)

    # Mantieni la colonna 'rating' nel risultato finale unendo nuovamente con ratings_df
    most_watched['rating'] = most_watched['avg_rating']
    

    # Ordina i film per il numero di valutazioni e prendi i primi 30
    sorted_items = most_watched.sort_values(by='num_ratings', ascending=False).head(30)
    

    # Genera raccomandazioni
    recommendationsMw = generate_recommendations(sorted_items)

    return jsonify(recommendationsMw)



def get_best_by_genre():
    from services import generate_recommendations
    # Carica i dati dai file CSV
    movies_df = load_movies(MOVIE_FILE_PATH)  # Contiene movieId, title, genres
    ratings_df = load_ratings(RATINGS_FILE_PATH)  # Contiene userId, movieId, rating, timestamp
    links_df = load_links(LINKS_FILE_PATH)  # Contiene movieId, imdbId, tmdbId

    # Calcola la media dei voti per ciascun movieId
    avg_ratings_df = ratings_df.groupby('movieId')['rating'].mean().reset_index()

    # Unisci i dati: movieId -> title, genres, rating
    data = pd.merge(movies_df, avg_ratings_df, on='movieId')  # Sostituisce i valori di rating con la media

    # Unisci i dati: movieId -> imdbId, tmdbId
    data = pd.merge(data, links_df, on='movieId')

    # Ottieni la lista di generi unici
    unique_genres = list(set(g for genre_list in data['genres'].dropna() for g in genre_list.split('|')))
    
    # Seleziona 6 generi casuali
    selected_genres = random.sample(unique_genres, 6)

    # Dizionario per salvare i film per ciascun genere
    recommendationsBg = []

    # Cicla sui generi selezionati
    for genre in selected_genres:
        # Filtra i film per il genere corrente
        genre_filtered = data[data['genres'].str.contains(genre, case=False, na=False)]

        # Escludi film con generi "(no genres listed)"
        genre_filtered = genre_filtered[genre_filtered['genres'] != "(no genres listed)"]

        if genre_filtered.empty:
            continue  # Salta il genere se non ci sono film

        # Rimuovi duplicati per movieId
        unique_movies = genre_filtered.drop_duplicates(subset='movieId')

        # Ordina i film per rating decrescente e prendi i primi 5
        sorted_items = unique_movies.sort_values(by='rating', ascending=False).head(5)

        # Genera raccomandazioni per il genere corrente
        recommendationsBg.extend(generate_recommendations(sorted_items))

        

    # Se nessun film è stato trovato per i generi selezionati
    if not recommendationsBg:
        return jsonify({'message': 'No movies found for the selected genres'}), 404

    # Restituisci tutte le raccomandazioni per ciascun genere
    return jsonify(recommendationsBg)



def get_random_recommendations():
    from services import generate_recommendations

    # Carica i dati dai file CSV
    ratings_df = load_ratings(RATINGS_FILE_PATH)  # Contiene userId, movieId, rating, timestamp
    movies_df = load_movies(MOVIE_FILE_PATH)  # Contiene movieId, title, genres
    links_df = load_links(LINKS_FILE_PATH)  # Contiene movieId, imdbId, tmdbId

    # Calcola la media dei voti per ciascun movieId
    avg_ratings_df = ratings_df.groupby('movieId')['rating'].mean().reset_index()

    # Unisci i dati: movieId -> title, genres, rating
    data = pd.merge(movies_df, avg_ratings_df, on='movieId')  # Sostituisce i valori di rating con la media

    # Unisci anche con links (movieId -> imdbId, tmdbId)
    data = pd.merge(data, links_df, on='movieId')

    # Elimina duplicati sui film (evita di avere più righe per lo stesso movieId)
    unique_movies = data.drop_duplicates(subset='movieId')

    # Seleziona casualmente 10 film
    random_movies = unique_movies.sample(n=30)

    # Formatta le raccomandazioni
    recommendationsRn = generate_recommendations(random_movies)

    return jsonify(recommendationsRn)


