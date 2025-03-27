from flask import Blueprint, render_template, session, redirect, url_for
from flask_jwt_extended import jwt_required
from ..user.forms import SignupForm, LoginForm
import os
import requests
from datetime import datetime

current_dir = os.path.abspath(os.path.dirname(__file__))

main_bp = Blueprint('main', __name__) 


if not  os.getenv('API_KEY'):
    print("API_KEY is not set in the environment variables")

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.themoviedb.org/3/'




@main_bp.route('/')
def index():

    url1 = f'{BASE_URL}movie/popular?api_key={API_KEY}&language=en-US&page=1'
    url2 = f'{BASE_URL}movie/top_rated?api_key={API_KEY}&language=en-US&page=1'

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    if response1.status_code == 200:
        most_reviewed = response1.json()['results']  # Get the movie results
        
    else:
        most_reviewed = []  

    if response2.status_code == 200:
        recent_reviewed = response1.json()['results']
        
    else:
         recent_reviewed = []

    
    most_reviewed_movies = most_reviewed[:10]
    recent_reviewed_movies = recent_reviewed[:10]

        

    return render_template('main/landing_page.html', MostReviewed=most_reviewed_movies, RecentReviewed= recent_reviewed_movies)


@main_bp.route('/dashboard/')
@jwt_required()
def dashboard():

    url1 = f'{BASE_URL}movie/now_playing?api_key={API_KEY}&language=en-US&page=1'
    url2 = f'{BASE_URL}movie/popular?api_key={API_KEY}&language=en-US&page=1'

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    
    if response1.status_code == 200:
        hightlight_movie = response1.json()['results'][0]
        
    else:
        hightlight_movie = []

    if response2.status_code == 200:
        trending_movies = response2.json()['results']
        
        recent_trending = [ movie for movie in trending_movies if datetime.strptime(movie['release_date'], '%Y-%m-%d').year > 2020][:5]
    else:
        trending_movies = []

    

    return render_template('main/Dashboard.html', HighlightMovie=hightlight_movie, TrendingMovies=recent_trending)


@main_bp.route('/movie_page/')
def movie_page():
    return render_template('main/frontend/movie_details.html')

