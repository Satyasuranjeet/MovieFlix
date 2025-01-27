from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from googleapiclient.discovery import build
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS for the Flask app
CORS(app)

# YouTube Data API credentials
API_KEY = os.getenv('YOUTUBE_API_KEY')  # Fetch the API key from the environment
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

CATEGORY_KEYWORDS = {
    'comedy': ['comedy', 'funny', 'humor'],
    'action': ['action', 'adventure', 'thriller'],
    'animation': ['animation', 'animated', 'cartoon'],
    'cartoon': ['cartoon', 'animated series'],
    'sci-fi': ['sci-fi', 'science fiction', 'space'],
    'fantasy': ['fantasy', 'magic', 'mythical'],
    'history': ['history', 'historical', 'biography']
}

def search_movies(query=None, category=None):
    """
    Search for movies on YouTube based on the input query and/or category.
    Returns a list of video URLs and thumbnails that are likely movies.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    # Build the search query
    search_query = ''
    if query:
        search_query += query
    if category and category in CATEGORY_KEYWORDS:
        search_query += ' ' + ' '.join(CATEGORY_KEYWORDS[category])

    search_response = youtube.search().list(
        q=search_query.strip(),
        part='snippet',
        type='video',
        videoDuration='long',  # Filter for long videos (indicates movies)
        videoDefinition='high',  # Filter for HD videos
        maxResults=50  # Fetch up to 50 results
    ).execute()

    results = []
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnail = item['snippet']['thumbnails']['high']['url']

        # Simple heuristic to filter movie-like videos
        if re.search(r'(full movie|official movie|\bmovie\b)', title, re.IGNORECASE) or \
           re.search(r'(full movie|official movie|\bmovie\b)', description, re.IGNORECASE):
            results.append({
                'title': title,
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'thumbnail': thumbnail
            })

    return results

@app.route('/search_movie', methods=['GET'])
def search_movie_api():
    """
    API endpoint to search for movies on YouTube.
    Accepts 'name' and/or 'category' parameters in the query string.
    """
    movie_name = request.args.get('name')
    category = request.args.get('category')

    if not movie_name and not category:
        return jsonify({'error': 'At least one of "name" or "category" parameters is required'}), 400

    try:
        results = search_movies(movie_name, category)
        if not results:
            return jsonify({'message': 'No movies found for the given criteria.'}), 404

        return jsonify({'movies': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_all', methods=['GET'])
def list_all_movies():
    """
    API endpoint to list all movies across categories.
    Fetches movies for all predefined categories.
    """
    all_movies = {}

    try:
        for category in CATEGORY_KEYWORDS:
            results = search_movies(category=category)
            all_movies[category] = results

        return jsonify({'all_movies': all_movies}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
