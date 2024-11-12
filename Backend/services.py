import requests
from config import TMDB_API_KEY, TMDB_BASE_URL

def get_movie_details(tmdb_id):
    tmdb_url = f'{TMDB_BASE_URL}/{tmdb_id}'
    response = requests.get(tmdb_url, params={'api_key': TMDB_API_KEY})
    return response.json()

def generate_recommendations(sorted_items):
    recommendations = []
    for _, row in sorted_items.iterrows():
        movie_data = get_movie_details(row['tmdbId'])

        genre_names = [genre['name'] for genre in movie_data.get('genres', [])]

        recommendations.append({
            'title': movie_data.get('title'),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'overview': movie_data.get('overview'),
            'genres': genre_names,
            'rating': row['rating'],
            'id': row['tmdbId']
        })
    return recommendations
