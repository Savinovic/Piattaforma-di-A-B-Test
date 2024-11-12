import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'


export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate= useNavigate();
  
  const { login, checkAuthStatus } = useAuth()

   // Esegui l'effetto una volta al caricamento

  if (loading) {
    return <p>Caricamento...</p>; // Mostra un messaggio di caricamento mentre controlli l'autenticazione
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h3>Login</h3>
        <div className="input-group">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <Link to="/signUp" className="link" style={{ color: 'white' }}>Non sei registrato? Registrati Qui!</Link>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};


