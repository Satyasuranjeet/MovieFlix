from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from dotenv import load_dotenv
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# YouTube Data API credentials
API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Expanded category keywords for better search results
CATEGORY_KEYWORDS = {
    'comedy': ['comedy movie', 'funny movie', 'comedy film', 'humorous movie'],
    'action': ['action movie', 'action film', 'adventure movie', 'thriller movie'],
    'animation': ['animated movie', 'animation film', 'animated feature'],
    'cartoon': ['cartoon movie', 'animated film', 'family movie'],
    'sci-fi': ['science fiction movie', 'sci-fi film', 'sci fi movie'],
    'fantasy': ['fantasy movie', 'fantasy film', 'magical movie'],
    'history': ['historical movie', 'history film', 'biography movie']
}

SERVER_START_TIME = time.time()

def create_youtube_client():
    """Create and return a YouTube API client."""
    try:
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    except Exception as e:
        logger.error(f"Failed to create YouTube client: {str(e)}")
        raise

def search_movies(query=None, category=None):
    """
    Search for movies using the YouTube Data API.
    
    Args:
        query (str, optional): Search query for movie title
        category (str, optional): Movie category to search for
        
    Returns:
        list: List of movie dictionaries containing title, URL, and thumbnail
    """
    try:
        youtube = create_youtube_client()
        
        # Build search query
        search_terms = []
        if query:
            search_terms.append(f"{query} full movie")
        if category and category in CATEGORY_KEYWORDS:
            search_terms.extend([f"{keyword}" for keyword in CATEGORY_KEYWORDS[category]])

        if not search_terms:
            search_terms = ["full movie"]  # Default search if no query/category provided

        all_results = []
        seen_video_ids = set()

        for search_term in search_terms:
            try:
                search_response = youtube.search().list(
                    q=search_term,
                    part='snippet',
                    type='video',
                    videoDuration='long',
                    videoDefinition='high',
                    maxResults=25,
                    relevanceLanguage='en'
                ).execute()

                for item in search_response.get('items', []):
                    video_id = item['id']['videoId']
                    
                    # Skip if we've already seen this video
                    if video_id in seen_video_ids:
                        continue
                        
                    title = item['snippet']['title']
                    thumbnail = (item['snippet']['thumbnails'].get('high', {}).get('url') or
                               item['snippet']['thumbnails'].get('medium', {}).get('url') or
                               item['snippet']['thumbnails'].get('default', {}).get('url'))

                    # Basic filtering for likely movie content
                    if any(term.lower() in title.lower() for term in ['movie', 'film', 'full']):
                        all_results.append({
                            'title': title,
                            'url': f'https://www.youtube.com/watch?v={video_id}',
                            'thumbnail': thumbnail
                        })
                        seen_video_ids.add(video_id)

                    # Break if we have enough results
                    if len(all_results) >= 10:
                        break

            except HttpError as e:
                logger.warning(f"YouTube API error during search: {str(e)}")
                if e.resp.status in [403, 429]:  # Quota exceeded or rate limit
                    break
                continue

        return all_results

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return []

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server status."""
    try:
        uptime = time.time() - SERVER_START_TIME
        youtube = create_youtube_client()
        return jsonify({
            'status': 'OK',
            'message': 'Server is running',
            'uptime': f'{uptime:.2f} seconds',
            'youtube_api': 'Connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': str(e)
        }), 500

@app.route('/search_movie', methods=['GET'])
def search_movie_api():
    """
    Main endpoint for searching movies.
    Accepts 'name' and/or 'category' as query parameters.
    """
    try:
        movie_name = request.args.get('name', '').strip()
        category = request.args.get('category', '').strip()

        # Log search request
        logger.info(f"Search request - name: {movie_name}, category: {category}")

        results = search_movies(movie_name, category)
        
        # Always return 200 with results array
        response_data = {
            'movies': results,
            'count': len(results)
        }
        
        if not results:
            response_data['message'] = 'No movies found matching your criteria'
        
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Search API error: {str(e)}")
        return jsonify({
            'movies': [],
            'error': 'An error occurred while searching for movies',
            'details': str(e)
        }), 200  # Still return 200 with empty results

@app.route('/popular_movies', methods=['GET'])
def popular_movies():
    """Endpoint to get popular movies across all categories."""
    try:
        results = search_movies()  # Search with no specific query
        return jsonify({
            'movies': results,
            'count': len(results)
        }), 200
    except Exception as e:
        logger.error(f"Popular movies error: {str(e)}")
        return jsonify({
            'movies': [],
            'error': str(e)
        }), 200

if __name__ == '__main__':
    # Set environment variables if not using .env file
    if not API_KEY:
        logger.warning("YouTube API key not found in environment variables")
        API_KEY = input("Please enter your YouTube API key: ")
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)