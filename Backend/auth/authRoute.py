from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from .userModel import User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Recupera i dati dal body della richiesta JSON
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Controlla se l'email esiste già
    if User.find_by_email(email):
        return jsonify({'error': 'User already exists'}), 400

    # Crea un nuovo utente con la password criptata
    
    new_user = User.create_user(username, email, password)
    
    login_user(new_user, remember=True)

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201


# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Recupera i dati dal body della richiesta JSON
    email = data.get('email')
    password = data.get('password')
    
    # Trova l'utente tramite l'email
    user = User.find_by_email(email)
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Effettua il login dell'utente
    print(f"Logging in user: {user.username}")

    login_user(user, remember=True)

    print(f"User {user.id} logged in successfully.")
    print(current_user.is_authenticated)
    

    next_page = request.args.get('next', '/home')
    
    return jsonify({'message': 'Login successful', 'user_id': user.id, 'assigned_test':user.assigned_test, 'next': next_page}), 200


# Logout route
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


# Verifica se l'utente è loggato (ad esempio quando si ricarica la pagina)
@auth_bp.route('/status', methods=['GET'])
def status():
    print(f"Session: {session}")  # Stampa il contenuto della sessione
    print(f"Current user: {current_user}")  # Stampa l'oggetto current_user
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'user_id': current_user.id, 'assigned_test':current_user.assigned_test}), 200
    else:
        return jsonify({'logged_in': False}), 200
