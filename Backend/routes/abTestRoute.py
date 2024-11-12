from flask import request, jsonify
from auth.userModel import User 
from config import VISUALIZATIONS
from algorithms import get_best_by_genre,get_most_watched, get_random_recommendations
import random

algorithm_mapping = {
    'get_random_recommendations': get_random_recommendations,
    'get_most_watched': get_most_watched,
    'get_best_by_genre': get_best_by_genre
}


def register_routes_ab(app):
    @app.route('/runABTest', methods=['POST'])
    def run_ab_test():
        user_id = request.json.get('user_id')  # Ottieni l'ID dell'utente dalla richiesta

        # Verifica che l'ID dell'utente sia stato fornito
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Verifica se l'utente esiste nel database
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Seleziona casualmente un algoritmo e un tipo di visualizzazione
        assigned_algorithm = random.choice(list(algorithm_mapping.keys()))

        assigned_visualization = random.choice(VISUALIZATIONS)

        # Crea l'oggetto `assigned_test` contenente entrambi
        assigned_test = {
            'algorithm': assigned_algorithm,
            'visualization': assigned_visualization
        }

        # Assegna il test all'utente e aggiorna il database
        User.assign_test_to_user(user_id, assigned_test)

        # Restituisci la risposta JSON con il test assegnato
        return jsonify({
            'user_id': user_id,
            'assigned_test': assigned_test
        }), 200
