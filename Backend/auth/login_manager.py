from flask_login import LoginManager
from datetime import timedelta
from .userModel import User  # Assicurati che il percorso del modello sia corretto

# Crea l'istanza di LoginManager
login_manager = LoginManager()


# Imposta la vista di login per le pagine protette
login_manager.login_view = 'auth.login'  # Modifica in base alla tua route di login

# Funzione per caricare l'utente dal database tramite user_id
@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with id: {user_id}")
    user= User.find_by_id(user_id)
    print(f"User found: {user}")
    return user
