from dotenv import load_dotenv
import os
import gdown
import pickle 
import streamlit as st
import requests

# ✅ Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# ✅ Download similarity.pkl from Google Drive if not present
similarity_file_path = 'model_data1/similarity.pkl'
file_id = '1QT2UYmbeSFrRx9s_omJkEESHPXyjyNZO'  # 🔑 Replace this with your actual Google Drive file ID
gdrive_url = f'https://drive.google.com/uc?id={file_id}'

# Create folder and download file
os.makedirs('model_data1', exist_ok=True)

if not os.path.exists(similarity_file_path):
    gdown.download(gdrive_url, similarity_file_path, quiet=False)

# ✅ Load pickled data
movies = pickle.load(open('model_data1/movie_list.pkl', 'rb'))
similarity = pickle.load(open(similarity_file_path, 'rb'))

# ✅ Streamlit page setup
st.set_page_config(layout="wide")

# ✅ CSS for dark theme
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
    .stApp {
        background-color: #F1F3F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ TMDB Poster API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""
    rating = data.get('vote_average', 'N/A')
    return full_path, rating

# ✅ Movie Recommendation Function
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

# ✅ Streamlit UI
st.header("🎬 Personalized Movie Recommendation System")

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
