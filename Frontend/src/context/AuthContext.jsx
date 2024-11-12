import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// Crea il contesto dell'autenticazione
const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

// Fornitore del contesto (AuthProvider)
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);   
  const [test, setTest]= useState(null);
  const [loading, setLoading] = useState(false);  // Stato di caricamento
  const [error, setError] = useState(null);       // Stato per gli errori
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Stato autenticazione
  const navigate = useNavigate();  // Per gestire la navigazione

  // Funzione di login
  const login = async (email, password) => {
    setLoading(true);  // Imposta lo stato di caricamento
    setError(null);    // Resetta eventuali errori
    try {
      const response = await axios.post('http://localhost:5000/auth/login', {
        email,
        password
      }, { withCredentials: true });  // Invio cookie di sessione
      
      if (response.data.message === 'Login successful') {
        setUser(response.data.user_id); 
        setIsAuthenticated(true);
        setTest(response.data.assigned_test)  // L'utente è autenticato
        navigate('/home');  // Reindirizza alla home page
      }
    } catch (err) {
      setError('Credenziali non valide, riprova.');
    } finally {
      setLoading(false);  // Fine del caricamento
    }
  };

  // Funzione di registrazione
  const signup = async (username, email, password) => {
    setLoading(true);  // Imposta lo stato di caricamento
    setError(null);    // Resetta eventuali errori
    try {
      const response = await axios.post('http://localhost:5000/auth/signup', {
        username,
        email,
        password
      }, { withCredentials: true });  // Invio cookie di sessione

      if (response.data.message === 'User created successfully') {
        setUser(response.data.user_id);
        setIsAuthenticated(true);  // L'utente è autenticato
        navigate('/vote');  // Reindirizza alla home page
        
      }
    } catch (err) {
      setError('Errore durante la registrazione, riprova.');
    } finally {
      setLoading(false);  // Fine del caricamento
    }
  };

  // Funzione di logout
  const logout = async () => {
    try {
      await axios.post('http://localhost:5000/auth/logout', {}, { 
        withCredentials: true  // Invia cookie di sessione per eseguire il logout
      });
      setUser(null);  // Rimuove l'utente dallo stato
      setIsAuthenticated(false);  // L'utente non è più autenticato
      navigate('/');  // Reindirizza alla pagina di login
    } catch (err) {
      console.error('Errore durante il logout:', err);
    }
  };

  // Funzione per controllare lo stato dell'utente (es. al caricamento della pagina)
  const checkAuthStatus = async () => {
    setLoading(true);  // Imposta lo stato di caricamento
    try {
      const response = await axios.get('http://localhost:5000/auth/status', {
        withCredentials: true  // Invia il cookie di sessione
      });

      if (response.data.logged_in) {
        setUser(response.data.user_id)
        setIsAuthenticated(true);
        setTest(response.data.assigned_test)  // L'utente è autenticato
        navigate('/home');  // Reindirizza alla home page
      } else {
        setIsAuthenticated(false);  // L'utente non è autenticato
      }
    } catch (err) {
      console.error('Errore nella verifica dello stato di autenticazione:', err);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);  // Fine del caricamento
    }
  };

  // Effettua il check dello stato dell'utente quando il componente viene montato
  useEffect(() => {
    checkAuthStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ user, test, setTest, loading, error, isAuthenticated, login, signup, logout, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};
