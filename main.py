from flask import Flask, render_template, request, jsonify
import json
from collections import defaultdict
import random

app = Flask(__name__)

# Load anime data
with open('anime_data.json', 'r') as f:
    anime_data = json.load(f)

def get_recommendations(user_anime):
    # Simple collaborative filtering
    genre_count = defaultdict(int)
    for anime in user_anime:
        if anime in anime_data:
            for genre in anime_data[anime]['genres']:
                genre_count[genre] += 1
    
    # Get top genres
    top_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Get recommendations based on top genres
    recommendations = []
    for anime, data in anime_data.items():
        if anime not in user_anime:
            if any(genre in data['genres'] for genre, _ in top_genres):
                recommendations.append(anime)
    
    return random.sample(recommendations, min(5, len(recommendations)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_anime = request.json['anime']
    recommendations = get_recommendations(user_anime)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)