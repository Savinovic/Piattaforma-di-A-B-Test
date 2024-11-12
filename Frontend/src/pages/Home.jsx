import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MovieItem from '../components/FilmCard';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';

const groupMoviesByGenre = (movies) => {
  return movies.reduce((acc, movie) => {
    // Assumendo che movie.genres sia un array di stringhe
    movie.genres.forEach((genre) => {
      if (!acc[genre]) {
        acc[genre] = [];
      }
      acc[genre].push(movie);
    });
    return acc;
  }, {});
};




export default function FilmRatings() {
  const [recommendations, setRecommendations] = useState([]); // Stato per memorizzare le raccomandazioni
  const [error, setError] = useState(null);
  const [userRatings, setUserRatings] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [isMobile, setIsMobile] = useState(false);
  const { logout, user, test,  loading } = useAuth();
  const [viewMode, setViewMode] = useState(test?.visualization || 'scroll'); // Aggiungi la nuova modalità qui
  const [isFetching, setIsFetching] = useState(true);

  const fetchUserRatings = async (user) => {
    try {
      const response = await axios.get(`http://localhost:5000/user-ratings`, {
        params: { user_id: user }
      });
      return response.data.votes;  // Presuppone che il backend restituisca i voti in un oggetto `votes`
    } catch (err) {
      console.error('Errore durante il recupero dei voti utente:', err);
      return {};  // Ritorna un oggetto vuoto in caso di errore
    }
  };

  const updateUserRatings = (movieId, rating) => {
    setUserRatings((prevRatings) => ({
      ...prevRatings,
      [movieId]: rating,
    }));
  };

  useEffect(() => {
    const updateIsMobile = () => {
      setIsMobile(window.innerWidth <= 768); // Ad esempio, 768px come soglia per mobile
    };
    updateIsMobile();
    window.addEventListener('resize', updateIsMobile);
    return () => window.removeEventListener('resize', updateIsMobile);
  }, []);

  const handleCardClick = (index) => {
    if (isMobile) {
      setHoveredIndex(hoveredIndex === index ? null : index);
    }
  };

  useEffect(() => {
    if (test) {
      setViewMode(test.visualization);
    }
  }, [test]);

  useEffect(() => {
    const loadUserRatings = async () => {
      const ratings = await fetchUserRatings(user);
      setUserRatings(ratings);
    };
    loadUserRatings();
  }, [user]);

  // Funzione per chiamare l'API Flask per le raccomandazioni
  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!user || !test) {
        console.log('Aspettando userId ');
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/recommendations', {
          params: { alg_test: test.algorithm },
        });
        setRecommendations(response.data)
        setIsFetching(false);  
      } catch (err) {
        setError('Errore durante il recupero dei dati delle raccomandazioni');
        console.error(err);
        setIsFetching(false);
      }
    };

    fetchRecommendations();
  }, [user]);

  const handleLogout = async (e) => {
    e.preventDefault();
    try {
      await logout();
    } catch (err) {
      console.error(err);
    }
  };

  const nextMovie = () => {
    if (currentIndex < recommendations.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const prevMovie = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  
  const currentBackdropPath =
    recommendations[currentIndex]?.backdrop_path
      ? `https://image.tmdb.org/t/p/w1280${recommendations[currentIndex].backdrop_path}`
      : '';

  const containerStyle = {
    backgroundImage: viewMode === 'scroll' && currentBackdropPath ? `url(${currentBackdropPath})` : 'none',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    padding: '20px',
    transition: 'background-image 0.5s ease-in-out',
  };

  if (loading || isFetching) {
    return <LoadingSpinner message="Caricamento delle raccomandazioni..." size={70} />;
  }

  const groupedRecommendations = viewMode === 'lines' ? groupMoviesByGenre(recommendations) : null;

  return (
    <div>

      <h1>POPCORN PICKS</h1>

      {error && <p>{error}</p>}
      <div className="toggle-button-container">
        <button onClick={handleLogout}>
          Logout
        </button>

      </div>

      {loading ? (
        <LoadingSpinner message="Caricamento in corso..." size={70} />
      ) : recommendations.length === 0 && !error ? (
        <LoadingSpinner message="Caricamento delle raccomandazioni..." size={70} />
      ) : viewMode === 'scroll' ? (
        <div className="movie-container" style={containerStyle}>
          <MovieItem movie={recommendations[currentIndex]} userRatings={userRatings} updateUserRatings={updateUserRatings}/>

          <div className="navigation-buttons">
            <button onClick={prevMovie} disabled={currentIndex === 0}>
              Precedente
            </button>
            <button onClick={nextMovie} disabled={currentIndex === recommendations.length - 1}>
              Successivo
            </button>
          </div>
        </div>
      ) : viewMode === 'list' ? (
        <div className="movie-list">
          {recommendations.map((movie, index) => (
            <div key={index}
              onMouseEnter={() => !isMobile && setHoveredIndex(index)}
              onMouseLeave={() => !isMobile && setHoveredIndex(null)}
              onClick={() => handleCardClick(index)}>
              <MovieItem key={index} movie={movie} isHidden={hoveredIndex !== index} userRatings={userRatings} updateUserRatings={updateUserRatings}/>
            </div>
          ))}
        </div>
      ) : (
        <div className="genres-container">
          {Object.entries(groupedRecommendations).map(([genre, movies]) => (
            <div key={genre} className="genre-section">
              <h3>{genre.toUpperCase()}</h3>
              <div className="movie-row">
                {movies.map((movie, index) => (
                  <MovieItem key={index} movie={movie} isCompact={viewMode ==='lines'} userRatings={userRatings} updateUserRatings={updateUserRatings}/>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
