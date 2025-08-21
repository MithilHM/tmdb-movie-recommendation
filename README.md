# TMDb Movie Recommendation Dashboard

An interactive movie recommendation web app leveraging The Movie Database (TMDb) API. The project features a Flask backend that provides movie search and recommendation APIs based on content similarity, and a Streamlit frontend dashboard for intuitive movie discovery and personalized recommendations.

## Features

- Search movies by title using TMDb API
- Content-based movie recommendation using TF-IDF and cosine similarity on movie descriptions
- Interactive Streamlit dashboard with movie details, posters, and recommendations
- Lightweight, no database required; all data fetched live from TMDb API
- Modular architecture with Flask backend API and Streamlit frontend UI
- Easily deployable to cloud platforms (e.g., Heroku for backend, Streamlit Community Cloud for frontend)

## Tech Stack

- Python 3.7+
- Flask (Backend API)
- Requests (HTTP client to TMDb API)
- Scikit-learn (TF-IDF vectorization and similarity)
- Streamlit (Frontend dashboard)
- TMDb API (free movie data API)

