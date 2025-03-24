import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=72e8468cfd36b851bac24cbae56317d4&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    recommended_movies = []
    recommended_movies_posters = []
    matches = movies_list[movies_list['title'].str.lower() == movie.lower()]
    if matches.empty:
        return ["Movie not found. Please select another one."]
    index = matches.index[0]  # Get movie index
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x: x[1])
    for i in distances[1:6]:
        movie_id = movies_list.iloc[i[0]].movie_id
        # Fetching poster from TMDB API as use the tmdb movies ID I currently have to fetch its poster and details.
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list)  # Convert back to DataFrame
movies_title = movies_list['title'].values  # Access the 'title' column
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('🎬 Movie Recommender System')

SelectedMovieName = st.selectbox(
    "How would you like to be contacted?",
    movies_title)

if st.button("Recommend"):
    names, posters = recommend(SelectedMovieName)

    cols = st.columns(len(names))
    for i in range(len(names)):
        with cols[i % 5]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)