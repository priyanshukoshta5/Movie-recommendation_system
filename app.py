import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="MOV -  RECMNDR - PriK",
    page_icon="🎥",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

my_tmdb_api = "8898c84128d63fa81eac49dbb8f8cb78"

def fetch_poster(id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(id, my_tmdb_api)
    response = requests.get(url)
    data = response.json()
    if data['poster_path'] == None:
        return "missing poster.jpg"
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie, movs):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:1+movs]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        recommended_movies.append(movies_list.iloc[i[0]].title)
        movie_id = movies_list.iloc[i[0]].id
        # Fetch poster using API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

# To run "streamlit run app.py" in terminal

selected_movie_name = st.selectbox(
    'Choose a movie-',
    movies)

st.write(" ")

movs = st.slider('How many movies to recommend?', min_value=5, max_value=25, value=5, step=5)


# st.write('You selected:', selected_movie_name)


if st.button('Recommend'):
    st.write(" ")
    names, posters = [], []
    with st.spinner('🔎 Searching...'):
        names, posters = recommend(selected_movie_name, movs)
    i = 0
    for temp in range(int(movs/5)):
        for col in st.columns(5):
            with col:
                st.write(names[i])
                st.image(posters[i])
            i = i+1
