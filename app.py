from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

import pickle 
import streamlit as st
import requests

st.set_page_config(layout="wide")

# Apply permanent dark theme using CSS
st.markdown(
    """
    <style>
    body {
        background-color: #F1F3F0;
        color: black;
    }
    img {
        width: 100% !important;
        height: auto;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)




def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    rating = data.get('vote_average', 'N/A')
    return full_path, rating


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True , key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    recommended_movies_rating = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating = fetch_poster(movie_id)
        recommended_movies_poster.append(poster)
        recommended_movies_rating.append(rating)
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster, recommended_movies_rating
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F1F3F0;
    }
    img {
        width: 100% !important;
        height: auto;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.header("🎬 Personalized Movie Recommendation System")
movies = pickle.load(open('model_data1/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model_data1/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    '🎥 Type or Select a movie for recommendation',
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ratings = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.image(recommended_movie_posters[idx], use_container_width=True)
        col.markdown(f"**{recommended_movie_names[idx]}**")
        col.markdown(f"⭐ Rating: {recommended_movie_ratings[idx]}")

