from flask import Flask, request, jsonify
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

TMDB_API_KEY = "398961f8f635303029a040e2610e75e3"
TMDB_API_BASE = "https://api.themoviedb.org/3"

def tmdb_search_movies(query, max_results=20):
    url = f"{TMDB_API_BASE}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query, "page": 1}
    response = requests.get(url, params=params).json()
    results = response.get("results", [])[:max_results]
    return results

def tmdb_get_popular_movies(max_results=50):
    url = f"{TMDB_API_BASE}/movie/popular"
    params = {"api_key": TMDB_API_KEY, "page": 1}
    response = requests.get(url, params=params).json()
    results = response.get("results", [])[:max_results]
    return results

@app.route("/search")
def search_movies():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    movies = tmdb_search_movies(query)
    return jsonify(movies)

@app.route("/recommendations")
def recommend_movies():
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return jsonify({"error": "movie_id parameter is required"}), 400

    # Get details for the selected movie
    url = f"{TMDB_API_BASE}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    movie_detail = requests.get(url, params=params).json()
    if "status_code" in movie_detail and movie_detail["status_code"] != 200:
        return jsonify({"error": "Movie not found"}), 404

    # Fetch popular movies as corpus for recommendation
    popular_movies = tmdb_get_popular_movies()

    # Prepare documents for TF-IDF: combine title + overview
    corpus = [f"{m['title']} {m.get('overview', '')}" for m in popular_movies]
    selected_movie_text = f"{movie_detail['title']} {movie_detail.get('overview', '')}"

    # Vectorize corpus + selected movie
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus + [selected_movie_text])

    # Calculate cosine similarity of selected movie with corpus
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Get top 5 most similar movies indices
    similar_indices = cosine_similarities.argsort()[-5:][::-1]

    recommended_movies = [popular_movies[i] for i in similar_indices]

    return jsonify(recommended_movies)

if __name__ == "__main__":
    app.run(debug=True)
#Add backend Flask app
