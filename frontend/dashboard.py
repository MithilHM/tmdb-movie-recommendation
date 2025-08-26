import streamlit as st
import requests

FLASK_API = "https://tmdb-flask-backend.onrender.com"

st.title("TMDb Movie Recommendation")

# Search movies
query = st.text_input("Search Movies by Title")
if query:
    res = requests.get(f"{FLASK_API}/search", params={"query": query})
    if res.status_code == 200:
        movies = res.json()
        if movies:
            movie_options = {f"{m['title']} ({m.get('release_date', 'N/A')[:4]})": m["id"] for m in movies}
            selected_movie = st.selectbox("Select a Movie", list(movie_options.keys()))
            movie_id = movie_options[selected_movie]

            if st.button("Get Recommendations"):
                rec_res = requests.get(f"{FLASK_API}/recommendations", params={"movie_id": movie_id})
                if rec_res.status_code == 200:
                    recommendations = rec_res.json()
                    st.subheader("Recommended Movies:")
                    for rec in recommendations:
                        st.markdown(f"**{rec['title']}** ({rec.get('release_date', 'N/A')[:4]})")
                        if rec.get('poster_path'):
                            st.image(f"https://image.tmdb.org/t/p/w200{rec['poster_path']}", width=100)
                        st.write(rec.get('overview', 'No description available'))
                else:
                    st.error("Failed to fetch recommendations")
        else:
            st.write("No movies found for this query")
    else:
        st.error("Search API failed")
#Add Streamlit frontend dashboard
