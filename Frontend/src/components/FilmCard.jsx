import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StarIcon from '@mui/icons-material/Star';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import { useAuth } from '../context/AuthContext';

export default function FilmCard({ movie, isHidden, isCompact, onVote, selected, userRatings, updateUserRatings }) {
  const [hoveredStars, setHoveredStars] = useState(0);
  const { user } = useAuth();

  const handleVote = async (rating) => {
    updateUserRatings(movie.id, rating);
    console.log(rating, movie.id, user)

    try {
      await axios.post('http://localhost:5000/submit-rating', {
        user_id: user,
        movie_id: movie.id,
        rating,
      });
      console.log('Voto inviato con successo!');
    } catch (err) {
      console.error('Errore durante l\'invio del voto:', err);
    }
  };

  let selectedStars = 0; // Inizializza a 0
  let isVoted = false; // Inizializza a false

  // Esegui questo blocco solo se `userRatings` è passato come props
  if (userRatings) {
    selectedStars = userRatings[movie.id] || 0;
    isVoted = selectedStars > 0;
  }

  return (
    <div className={`movie-item ${isCompact ? 'compact' : ''}`}>
      <div className={`movie-left ${isCompact ? 'compact' : ''}`}>
        <h2>{movie.title}</h2>
        <img
          src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
          alt={`${movie.title} Poster`}
          width={isCompact ? '100' : '200'}
        />
        <p>
          <TrendingUpIcon style={{ color: 'yellow' }} /> {movie.rating.toFixed(2)}
        </p>

        {!onVote && (
          <div className="star-vote">
            {[1, 2, 3, 4, 5].map((star) => (
              <StarIcon
                key={star}
                style={{
                  color: star <= (hoveredStars || selectedStars) ? 'yellow' : 'gray',
                  cursor: isVoted ? 'default' : 'pointer',
                }}
                onMouseEnter={() => !isVoted && setHoveredStars(star)}
                onMouseLeave={() => setHoveredStars(0)}
                onClick={() => !isVoted && handleVote(star)}
              />
            ))}
          </div>
        )}

        {/* Mostra i pulsanti solo se la funzione onVote è stata passata */}
        {onVote && (
          <div className="vote-buttons">
            <button
              onClick={() => onVote(movie.id)}
              className={selected ? 'selected' : ''}
            >
              👍 Mi è piaciuto
            </button>
          </div>
        )}
      </div>
      {!isHidden && !isCompact && (
        <div className="movie-right">
          {movie.overview}
        </div>
      )}
    </div>
  );
}





