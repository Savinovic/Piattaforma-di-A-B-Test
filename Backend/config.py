import os
from algorithms import get_best_by_genre, get_most_watched, get_random_recommendations

TMDB_API_KEY = 'd6ecf84e63caaf24ec0fc382dbd3a3ff'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/movie'


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://utenteProva:utenteProva123@cluster0.3iblz3a.mongodb.net/Users?retryWrites=true&w=majority&appName=Cluster0')

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

VISUALIZATIONS = ['scroll', 'list', 'lines']