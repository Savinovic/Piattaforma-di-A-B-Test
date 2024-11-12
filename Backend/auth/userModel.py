from flask import session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId

def find_by_id(user_id):
    # Convertire user_id a ObjectId prima di cercare
    user_data = users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

def get_next_user_id():
    # Utilizza la collezione counters per tracciare l'ultimo userId
    counter = counters.find_one_and_update(
        {"_id": "userId"},  # L'ID per il contatore userId
        {"$inc": {"sequence_value": 1}},  # Incrementa il valore del contatore
        upsert=True,  # Crea il documento se non esiste
        return_document=True  # Restituisce il nuovo documento aggiornato
    )
    
    # Restituisce il nuovo valore di userId
    return counter['sequence_value']


# Inizializza il bcrypt
bcrypt = Bcrypt()

# Configurazione MongoDB
client = MongoClient("mongodb+srv://utenteProva:utenteProva123@cluster0.3iblz3a.mongodb.net/Users?retryWrites=true&w=majority&appName=Cluster0")  # Inserisci la tua connessione MongoDB
db = client['user_db2']
users = db['users1']
counters = db['counters']

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.assigned_test = user_data.get('assigned_test')
        

    @staticmethod
    def find_by_email(email):
        user_data = users.find_one({"email": email})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def create_user(username, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        

        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        users.insert_one(user_data)
        return User(user_data)

    def find_by_id(user_id):
        user_data = users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None
    
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    
    @staticmethod
    def assign_test_to_user(user_id, assigned_test):
        """
        Assegna un test specifico a un utente nel database e restituisce un JSON di risposta.
        :param user_id: L'ID dell'utente al quale assegnare il test.
        :param assigned_test: Il test da assegnare all'utente (un dizionario con le informazioni sul test).
        :return: Un JSON contenente l'ID dell'utente e il test assegnato.
        """
        # Aggiornamento dell'utente nel database
        result = users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"assigned_test": assigned_test}}
        )

        # Verifica se l'aggiornamento è andato a buon fine
        if result.modified_count > 0:
            return jsonify({
                'user_id': str(user_id),  # Restituisce l'ID dell'utente come stringa
                'assigned_test': assigned_test
            })
        else:
            return jsonify({"error": "Failed to assign test."}), 500
    