from flask import Flask
from flask_cors import CORS
from routes.recommendationsRoute import register_routes
from routes.voteRoute import register_voting_routes
from routes.abTestRoute import register_routes_ab
from auth.authRoute import auth_bp
from auth.login_manager import login_manager
from config import SECRET_KEY
from datetime import timedelta


app = Flask(__name__)
CORS(app,supports_credentials=True, origins=["http://localhost:3000"])

app.config['SESSION_PERMANENT'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Consenti l'uso del cookie in richieste cross-origin
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = SECRET_KEY

login_manager.init_app(app)

# Registra le rotte
register_routes(app)
register_voting_routes(app)
register_routes_ab(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
