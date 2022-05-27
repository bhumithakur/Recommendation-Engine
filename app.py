import streamlit as st
import json
from Classifier import   KNearestNeighbours
from operator import itemgetter


# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)


def knn(test_point, k):
     
    target = [0 for item in movie_titles]
     
    model =   KNearestNeighbours(data, target, test_point, k=k)
  
    model.fit()
     
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    
    table = list()
    for i in model.indices:
         
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    st.header('Movie Recommendation System')
    apps = ['--Select--', 'Recommedation Based On Movies ', 'Recommedation Based On Genres']
    app_options = st.selectbox('Select application:', apps)
    if app_options ==  apps[1]:
        movie_select = st.selectbox('Select movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Select a movie')
        else:
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[2]:
        options = st.multiselect('Select genres:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            n = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
        else:
            st.write("This is a  Movie Recommendtion application. "
                     "Here , You Can SSelect based On Movies and based On Genres.")
    else:
        st.write('Select option')
