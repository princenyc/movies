import streamlit as st
import requests

API_KEY = 'your_tmdb_api_key'  # Replace this with your TMDB API key
TMDB_BASE = 'https://api.themoviedb.org/3'

def search_movie(title):
    url = f"{TMDB_BASE}/search/movie"
    params = {'api_key': API_KEY, 'query': title}
    response = requests.get(url, params=params).json()
    return response['results'][0] if response['results'] else None

def get_similar_movies(movie_id):
    url = f"{TMDB_BASE}/movie/{movie_id}/similar"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params).json()
    return response['results'][:3]

def get_poster_url(poster_path):
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"

# — Streamlit App —
st.set_page_config(page_title="🎬 Movie Matchmaker", layout="centered")
st.title("🎬 Movie Matchmaker")
st.write("Enter a movie title, and we’ll recommend 3 similar films based on vibe and style.")

movie_title = st.text_input("🍿 Movie Title")

if st.button("🔍 Recommend Movies"):
    if not movie_title:
        st.error("Please enter a movie title.")
    else:
        with st.spinner("Finding movie matches..."):
            movie = search_movie(movie_title)

        if movie:
            st.success(f"Found: {movie['title']} ({movie['release_date'][:4]})")
            st.image(get_poster_url(movie.get('poster_path')), width=200)
            st.markdown(f"**{movie['overview']}**")

            similar_movies = get_similar_movies(movie['id'])

            st.markdown("### 🎥 Similar Movies")
            for sim in similar_movies:
                st.image(get_poster_url(sim.get('poster_path')), width=150)
                st.markdown(f"**{sim['title']}** ({sim['release_date'][:4]})")
                st.caption(sim.get('overview', 'No description available.'))
                st.markdown("---")
        else:
            st.warning("Movie not found. Please check your spelling or try another title.")
