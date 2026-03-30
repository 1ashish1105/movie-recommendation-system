from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


@app.route('/', methods=['GET', 'POST'])
def home():
    recommended = []

    if request.method == 'POST':
        movie = request.form.get('movie')
        recommended = recommend(movie)

    movie_list = movies['title'].values

    return render_template('index.html', movie_list=movie_list, recommended=recommended)


if __name__ == '__main__':
    app.run(debug=True)