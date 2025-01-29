import React, { useState, useEffect } from 'react';
import { Search, X, Volume2, Settings, Download, Maximize2 } from 'lucide-react';

// Server Wake-up Loading Screen Component
const ServerWakeupScreen = () => (
  <div className="fixed inset-0 bg-[#1E1E1E] flex flex-col items-center justify-center z-50">
    <div className="w-24 h-24 mb-8 relative">
      <div className="absolute inset-0 border-4 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
      <div className="absolute inset-2 border-4 border-teal-400 border-t-transparent rounded-full animate-spin-slow"></div>
    </div>
    <h2 className="text-2xl font-bold text-white mb-4">Starting up MovieFlix</h2>
    <p className="text-gray-400 text-center max-w-md px-4">
      Our server is waking up from hibernation. This might take up to 30 seconds. 
      Thank you for your patience!
    </p>
  </div>
);

// MovieCard Component
const MovieCard = ({ movie, onClick, onDownload }) => (
  <div 
    className="relative group cursor-pointer rounded-lg overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-xl"
  >
    <img 
      src={movie.thumbnail} 
      alt={movie.title}
      className="w-full h-48 object-cover"
      onClick={() => onClick(movie)}
    />
    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
      <h3 className="text-white font-bold text-sm line-clamp-2">
        {movie.title}
      </h3>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onDownload(movie);
        }}
        className="mt-2 text-teal-400 hover:text-teal-300 flex items-center gap-2"
      >
        <Download size={16} />
        <span className="text-sm">Download</span>
      </button>
    </div>
  </div>
);

// VideoPlayer Component
const VideoPlayer = ({ url }) => (
  <div className="relative aspect-video bg-black rounded-lg overflow-hidden">
    <iframe
      src={url.replace('watch?v=', 'embed/')}
      className="w-full h-full"
      allowFullScreen
    />
    <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black to-transparent">
      <div className="flex items-center justify-between text-white">
      </div>
    </div>
  </div>
);

// Modal Component
const Modal = ({ isOpen, onClose, children, title }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg max-w-[800px] w-full">
        <div className="flex justify-between items-center p-4 border-b border-gray-800">
          <h2 className="text-white text-lg font-bold">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X size={24} />
          </button>
        </div>
        <div className="p-4">
          {children}
        </div>
      </div>
    </div>
  );
};

// Main App Component
const MovieSearchApp = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [category, setCategory] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [isServerReady, setIsServerReady] = useState(false);

  const categories = [
    'comedy', 'action', 'animation', 'cartoon', 'sci-fi', 'fantasy', 'history'
  ];

  // Check server status on initial load
  useEffect(() => {
    const checkServerStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/health');
        if (response.ok) {
          setIsServerReady(true);
        } else {
          setTimeout(checkServerStatus, 2000);
        }
      } catch (error) {
        setTimeout(checkServerStatus, 2000);
      }
    };

    checkServerStatus();
  }, []);

  const handleDownload = async (movie) => {
    try {
      const response = await fetch(movie.url);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${movie.title}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download the movie. Please try again.');
    }
  };

  const fetchMovies = async () => {
    setLoading(true);
    setError(null);
    setHasSearched(true);
    
    try {
      const params = new URLSearchParams();
      
      if (searchQuery.trim()) {
        params.append('name', searchQuery.trim());
      }
      if (category) {
        params.append('category', category);
      }

      const response = await fetch(`https://movieflix-dknn.onrender.com/search_movie?${params}`);
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
        setMovies([]);
      } else {
        setMovies(data.movies || []);
      }
    } catch (err) {
      setError('Failed to fetch movies. Please try again.');
      setMovies([]);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };    

  // Show loading screen if server is not ready
  if (!isServerReady) {
    return <ServerWakeupScreen />;
  }

  return (
    <div className="min-h-screen bg-[#1E1E1E]">
      {/* Header */}
      <header className="bg-gradient-to-r from-gray-900 to-gray-800 py-6">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-center text-white">
            MovieFlix
          </h1>
          <p className="text-center text-gray-400 mt-2">
            Find your favorite movies in just seconds!
          </p>
        </div>
      </header>

      {/* Search Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Search movies by name..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setCategory('');
                }}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    fetchMovies();
                  }
                }}
                className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
              <Search className="absolute right-3 top-2.5 text-gray-400" size={20} />
            </div>
          </div>
          <select
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setSearchQuery('');
            }}
            className="w-full md:w-48 px-4 py-2 bg-gray-800 text-white rounded-lg border border-gray-700 focus:ring-2 focus:ring-teal-500 focus:outline-none"
          >
            <option value="">Select Category</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
          <button
            onClick={fetchMovies}
            className="px-6 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition-colors"
          >
            Search
          </button>
        </div>
      </div>

      {/* Results Section */}
      <div className="container mx-auto px-4 py-8">
        {!hasSearched ? (
          <div className="text-center py-12">
            <h2 className="text-2xl font-bold text-white mb-4">Welcome to MovieFlix!</h2>
            <p className="text-gray-400">
              Search for movies by name or browse by category to get started.
            </p>
          </div>
        ) : loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
          </div>
        ) : error ? (
          <div className="text-red-500 text-center py-12">{error}</div>
        ) : movies.length === 0 ? (
          <div className="text-gray-400 text-center py-12">No movies found</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {movies.map((movie, index) => (
              <MovieCard
                key={index}
                movie={movie}
                onClick={setSelectedMovie}
                onDownload={handleDownload}
              />
            ))}
          </div>
        )}
      </div>

      {/* Video Modal */}
      <Modal
        isOpen={!!selectedMovie}
        onClose={() => setSelectedMovie(null)}
        title={selectedMovie?.title}
      >
        {selectedMovie && <VideoPlayer url={selectedMovie.url} />}
      </Modal>
    </div>
  );
};

export default MovieSearchApp;