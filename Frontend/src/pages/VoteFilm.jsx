import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MovieItem from '../components/FilmCard';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';

export default function FilmVotingPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);
  const [isSecondVote, setIsSecondVote] = useState(false);
  const { user, test, setTest, loading } = useAuth();
  const [selectedMovies, setSelectedMovies] = useState([]); // Stato per memorizzare i voti dei film
  const [isFetchingRecommendations, setIsFetchingRecommendations] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      console.log('Aspettando userId');
      return; // Non fare nulla finché user non è disponibile
    }
    const fetchRecommendations = async () => {
      if (!user) {
        console.log('Aspettando userId ');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/votingRecommendations');
        setRecommendations(response.data);
      } catch (err) {
        setError('Errore durante il recupero dei dati delle raccomandazioni');
        console.error(err);
      }
    };

    fetchRecommendations();
  }, [user]);

  // Funzione per gestire la selezione di un film piaciuto
  const handleVote = (movieId) => {
    setSelectedMovies((prevSelected) => {
      if (prevSelected.includes(movieId)) {
        // Se il film è già selezionato, lo deseleziona (toggle)
        return prevSelected.filter((id) => id !== movieId);
      } else {
        // Altrimenti, lo seleziona
        return [...prevSelected, movieId];
      }
    });
  };

  // Funzione per inviare i voti al server
  const submitVotes = async () => {
    // Imposta i voti per tutti i film: 1 per i selezionati, -1 per i non selezionati
    const votes = recommendations.map((movie) => ({
      movieId: movie.id,
      vote: selectedMovies.includes(movie.id) ? 1 : -1,
    }));

    try {
      await axios.post('http://localhost:5000/submit-votes', {
        user,
        votes,
      });
      console.log('Voti inviati con successo!');
    } catch (err) {
      console.error('Errore durante l\'invio dei voti:', err);
    }
  };

  // Funzione per recuperare nuovi consigli basati sui voti dell'utente
  const fetchNewRecommendations = async () => {
    setIsFetchingRecommendations(true);
    try {
      const response = await axios.get(`http://localhost:5000/recommend-based-on-votes`,{params: { user_id: user }});
      setRecommendations(response.data);  // Aggiorna la lista dei film consigliati
    } catch (err) {
      console.error('Errore durante il recupero dei nuovi consigli:', err);
    }
    setIsFetchingRecommendations(false);
  };

  const abTest = async () => {
    try {
      const abTestResponse = await axios.post('http://localhost:5000/runABTest', {
        user_id: user,
      });
      console.log("AB test triggered:", abTestResponse.data);
      setTest(abTestResponse.data.assigned_test)
      console.log(test)
    } catch (abTestError) {
      console.error("Error triggering AB test:", abTestError);
    }  // Reindirizza alla home page
  }



  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isSecondVote) {
      // Prima votazione: invia i voti e ottieni i nuovi film consigliati
      await submitVotes(e);
      await abTest(e);
      await fetchNewRecommendations();  // Aggiorna i film consigliati
      setIsSecondVote(true);            // Passa alla seconda votazione
    } else {
      // Seconda votazione: invia i voti e reindirizza alla pagina successiva
      await submitVotes();
      navigate('/home');  // Cambia '/next-content' con il percorso della pagina successiva
    }
  };

  return (
    <div>
      <h1>Vota i tuoi Film Preferiti</h1>

      {error && <p>{error}</p>}

      {loading ? (
        <LoadingSpinner message="Caricamento in corso..." size={50} />
      ) : isFetchingRecommendations ? (
        <LoadingSpinner message="Caricamento di nuovi consigli basati sui tuoi voti..." size={50} />
      ): recommendations.length === 0 && !error ? (
        <LoadingSpinner message="Caricamento delle raccomandazioni..." size={50} />
      ) : (
        <div className="movie-list vote-view">
          {recommendations.map((movie, index) => (
            <MovieItem key={index} movie={movie} onVote={handleVote} selected={selectedMovies.includes(movie.id)} />
          ))}
        </div>
      )}
      <div className="toggle-button-container">
        <button onClick={handleSubmit}>
          Invia Voti
        </button>
      </div>
    </div>
  );
}
