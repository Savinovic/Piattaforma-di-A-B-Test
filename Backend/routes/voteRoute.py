from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
import pandas as pd
from algorithms import get_random_recommendations
from utils import load_ratings, load_links, load_movies
from settings import RATINGS_FILE_PATH, LINKS_FILE_PATH, MOVIE_WITH_TAGS_FILE_PATH

def register_voting_routes(app):
    # Connessione al database MongoDB
    client = MongoClient("mongodb+srv://utenteProva:utenteProva123@cluster0.3iblz3a.mongodb.net/Users?retryWrites=true&w=majority&appName=Cluster0")
    db = client["film_database"]
    votes_collection = db["votes"]
    rating_collection = db["rating"]

    # Simulazione del contenuto di TESTS e della mappatura degli algoritmi

    # Rotta per ottenere raccomandazioni
    @app.route('/votingRecommendations', methods=['GET'])
    def run_recommendation_voting():
        recommendations= get_random_recommendations()
        

        return recommendations

    # Rotta per il salvataggio dei voti
    @app.route('/submit-votes', methods=['POST'])
    def submit_votes():
        # Estrai i dati JSON dalla richiesta
        data = request.get_json()

        # Controllo per i dati mancanti
        if not data or 'user' not in data or 'votes' not in data:
            return jsonify({'error': 'Dati mancanti'}), 400

        user_id = data['user']
        votes = data['votes']

        # Salva o aggiorna ogni voto nel database MongoDB
        votes_collection.update_one(
            {'userId': user_id},  # Cerca il documento basato sull'userId
            {'$set': {'userId': user_id, 'votes': votes}},  # Imposta o aggiorna i voti
            upsert=True  # Crea un nuovo documento se non esiste
        )

        # Restituisci una risposta di successo
        return jsonify({'message': 'Voti salvati con successo'}), 200
    
    @app.route('/submit-rating', methods=['POST'])
    def submit_rating():
        # Estrai i dati JSON dalla richiesta
        data = request.get_json()

        # Controllo per i dati mancanti
        if not data or 'user_id' not in data or 'movie_id' not in data or 'rating' not in data:
            return jsonify({'error': 'Dati mancanti'}), 400

        user_id = data['user_id']
        movie_id = data['movie_id']
        rating = data['rating']

        # Salva o aggiorna il voto nel documento dell'utente
        rating_collection.update_one(
            {'_id': user_id},  # Cerca il documento basato sull'userId
            {
                '$set': {
                    f'votes.{movie_id}': rating  # Aggiorna il voto per il film specifico
                }
            },
            upsert=True  # Crea un nuovo documento se non esiste
        )

       # Restituisci una risposta di successo
        return jsonify({'message': 'Voto salvato con successo'}), 200
    
    @app.route('/user-ratings', methods=['GET'])
    def get_user_ratings():
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({'error': 'user_id mancante'}), 400

        # Trova il documento dell'utente con i voti
        user_votes = rating_collection.find_one({'_id': user_id}, {'_id': 0, 'votes': 1})

        if not user_votes:
            return jsonify({'votes': {}})  # Ritorna un oggetto vuoto se l'utente non ha voti

        return jsonify({'votes': user_votes.get('votes', {})}), 200
    
    @app.route('/recommend-based-on-votes', methods=['GET'])
    def recommend_based_on_votes():
        user_id = request.args.get('user_id')
        from services import generate_recommendations

        if not user_id:
            return jsonify({'error': 'user_id mancante'}), 400

        # Recupera i voti dell'utente per i film con voto pari a 1
        user_votes = votes_collection.find_one({'userId': user_id}, {'votes': 1})
        if not user_votes:
           print(f"Voti dell'utente recuperati: {user_votes}")
           return jsonify({'recommendations': []})
        
        print(f"Voti dell'utente recuperati: {user_votes}")


        # Filtra solo i film con voto 1
        liked_movies_ids = [vote['movieId'] for vote in user_votes['votes'] if vote['vote'] == 1]

        # Se non ci sono film votati positivamente, restituisci una lista vuota
        if not liked_movies_ids:
            print(f"Film piaciuti dall'utente: {liked_movies_ids}")
            return jsonify({'recommendations': []})
        print(f"Film piaciuti dall'utente: {liked_movies_ids}")


        # Carica il dataset dei film (inclusi attori, keywords, setting, ecc.)
        ratings_df = load_ratings(RATINGS_FILE_PATH)  # Contiene userId, movieId, rating
        movies_df = load_movies(MOVIE_WITH_TAGS_FILE_PATH)      # Contiene movieId, title, genres, actors, keywords, setting
        links_df = load_links(LINKS_FILE_PATH)        # Contiene movieId, imdbId, tmdbId

        # Calcola la media dei voti per ciascun movieId
        avg_ratings_df = ratings_df.groupby('movieId')['rating'].mean().reset_index()

        # Unisci i dati: movieId -> title, genres, rating
        data = pd.merge(movies_df, avg_ratings_df, on='movieId')  # Sostituisce i valori di rating con la media

        # Unisci anche con links (movieId -> imdbId, tmdbId)
        data = pd.merge(data, links_df, on='movieId')

        # Elimina duplicati sui film (evita di avere più righe per lo stesso movieId)
        movies = data.drop_duplicates(subset='movieId')
        print(f"Dati unisci: {movies}")

        # Recupera i dettagli dei film che l'utente ha votato positivamente
        liked_movies = movies[movies['tmdbId'].isin(liked_movies_ids)]
        print(f"Film piaciuti dall'utente 2: {liked_movies}")


         # Definisci le caratteristiche per il confronto
        characteristics = ['actors', 'keywords', 'setting']

        # Filtra i film simili esclusi quelli votati dall'utente
        similar_movies = movies[
            ~movies['tmdbId'].isin(liked_movies_ids) &  # Esclude i film già votati
            movies.apply(lambda row: any(
                row[char] in liked_movies[char].values for char in characteristics
            ), axis=1)
        ]
        print(f"Film simili: {similar_movies}")

        # Seleziona casualmente 10 film dai film simili trovati
        recommendations = similar_movies.sample(n=10)
  
        # Prepara i dati da restituire
        recommendationsNew = generate_recommendations(recommendations)
        return jsonify(recommendationsNew)



