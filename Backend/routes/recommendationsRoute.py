from flask import request, jsonify, Response
from algorithms import get_best_by_genre,get_most_watched, get_random_recommendations

import random

algorithm_mapping = {
    'get_random_recommendations': get_random_recommendations,
    'get_most_watched': get_most_watched,
    'get_best_by_genre': get_best_by_genre
}

def register_routes(app):
    @app.route('/recommendations', methods=['GET'])
    def run_recommendation_test():
        # Recupera il test dalla richiesta
        
        alg_test = request.args.get('alg_test')

        # Verifica se il test_id è stato fornito
        if not alg_test:
            return jsonify({'error': 'Test ID is required'}), 400

        # Trova il test corrispondente nel file di configurazione
        selected_alg = next((test for test in algorithm_mapping if test == alg_test), None)

        # Verifica se il test esiste
        if not selected_alg:
            return jsonify({'error': 'Invalid test Algorithm'}), 404


        # Usa globals() per ottenere la funzione dall'algoritmo specificato come stringa
        algorithm = algorithm_mapping.get(selected_alg)

            # Verifica se l'algoritmo esiste
        if algorithm:
            recommendations = algorithm()
        else:
            return jsonify({'error': 'Algorithm not found'}), 500

        # Restituiamo il risultato
        return recommendations

