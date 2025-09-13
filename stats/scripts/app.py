#!/usr/bin/env python3
"""
Flask Backend for Wrestling News Hub
Provides API endpoint to fetch tweets from X/Twitter API
"""

import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
USERNAME = 'JesseRodPodcast'
MAX_TWEETS = 5

def get_user_id(username, bearer_token):
    """Get user ID from username using Twitter API v2"""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data']['id']
    except Exception as e:
        logger.error(f"Error getting user ID for {username}: {e}")
        return None

def fetch_tweets(user_id, bearer_token, max_results=5):
    """Fetch recent tweets from user using Twitter API v2"""
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }
    
    params = {
        'max_results': max_results,
        'tweet.fields': 'created_at,public_metrics',
        'exclude': 'retweets,replies'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        tweets = []
        for tweet in data.get('data', []):
            tweets.append({
                'text': tweet['text'],
                'url': f"https://x.com/{USERNAME}/status/{tweet['id']}",
                'created_at': tweet['created_at'],
                'id': tweet['id']
            })
        
        return tweets
    except Exception as e:
        logger.error(f"Error fetching tweets: {e}")
        return []

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    """API endpoint to fetch recent tweets"""
    try:
        # Check if Bearer Token is available
        if not TWITTER_BEARER_TOKEN:
            logger.warning("Twitter Bearer Token not found, returning sample data")
            return jsonify(get_sample_tweets())
        
        # Get user ID
        user_id = get_user_id(USERNAME, TWITTER_BEARER_TOKEN)
        if not user_id:
            logger.warning("Could not get user ID, returning sample data")
            return jsonify(get_sample_tweets())
        
        # Fetch tweets
        tweets = fetch_tweets(user_id, TWITTER_BEARER_TOKEN, MAX_TWEETS)
        
        if not tweets:
            logger.warning("No tweets fetched, returning sample data")
            return jsonify(get_sample_tweets())
        
        logger.info(f"Successfully fetched {len(tweets)} tweets")
        return jsonify(tweets)
        
    except Exception as e:
        logger.error(f"Error in /api/tweets endpoint: {e}")
        return jsonify(get_sample_tweets()), 500

def get_sample_tweets():
    """Return sample wrestling-related tweets for demonstration"""
    return [
        {
            "text": "🎙️ New episode dropping tomorrow! Breaking down the latest WWE storylines and what's next for CM Punk in Chicago.",
            "url": "https://x.com/JesseRodPodcast/status/123456789",
            "created_at": "2024-09-12T10:00:00Z",
            "id": "123456789"
        },
        {
            "text": "That AJ Lee return was INSANE! Wrestling fans, we need to talk about this game-changing moment on SmackDown.",
            "url": "https://x.com/JesseRodPodcast/status/123456790",
            "created_at": "2024-09-12T08:00:00Z",
            "id": "123456790"
        },
        {
            "text": "John Cena's farewell tour hits different in Chicago. The emotion, the history, the legacy. Full breakdown coming soon! 🏆",
            "url": "https://x.com/JesseRodPodcast/status/123456791",
            "created_at": "2024-09-11T15:00:00Z",
            "id": "123456791"
        },
        {
            "text": "Behind the scenes: Preparing for a huge interview with a wrestling industry insider. This one's going to be special! 🤼‍♂️",
            "url": "https://x.com/JesseRodPodcast/status/123456792",
            "created_at": "2024-09-11T12:00:00Z",
            "id": "123456792"
        },
        {
            "text": "WrestleMania 40 predictions are heating up! Who do you think will main event? Drop your thoughts below! 🎯",
            "url": "https://x.com/JesseRodPodcast/status/123456793",
            "created_at": "2024-09-10T18:00:00Z",
            "id": "123456793"
        }
    ]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Wrestling News Hub API',
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Wrestling News Hub API',
        'endpoints': {
            '/api/tweets': 'GET - Fetch recent tweets',
            '/api/health': 'GET - Health check'
        },
        'username': USERNAME,
        'max_tweets': MAX_TWEETS
    })

if __name__ == '__main__':
    # Check for Bearer Token
    if not TWITTER_BEARER_TOKEN:
        logger.warning("TWITTER_BEARER_TOKEN environment variable not set")
        logger.info("API will return sample data. Set TWITTER_BEARER_TOKEN to fetch real tweets.")
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Wrestling News Hub API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
