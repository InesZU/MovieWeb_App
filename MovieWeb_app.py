import requests
from flask import Flask, flash, request, render_template, redirect, url_for
from datamanager import SQLiteDataManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

# Initialize SQLiteDataManager with the path to your SQLite database
data_manager = SQLiteDataManager("movieweb_app.sqlite")
API_KEY = os.environ.get('OMDBAPI_KEY')
API_URL = "http://www.omdbapi.com/"


def fetch_movie_details(title, api_key=API_KEY):
    """
    Fetch movie details from the OMDb API if the movie is not found in the local storage.
    This function is primarily used as a backup when a movie is not found in the local
    JSON file.

    Parameters:
        title (str): The title of the movie to fetch.
        api_key (str): The API key used to access the OMDb API.

    Returns:
        dict or None: A dictionary containing movie details if the movie is found,
                      otherwise None if the movie is not found or if there's an error.
    """
    url = f"{API_URL}?apikey={api_key}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['Response'] == 'False':
            return None  # Movie not found
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the OMDb API: {e}")
        return None


@app.route('/')
def home():
    """
    Route for the home page.

    Returns:
        Rendered 'home.html' template.
    """
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    Route to get all registered users.

    Returns:
        Rendered 'users.html' template displaying the list of users.
    """
    users = data_manager.get_all_users()
    users_list = [{"id": user.id, "name": user.name} for user in users]
    return render_template('users.html', users=users_list)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Route to display movies for a specific user.

    Args:
        user_id (int): ID of the user whose movies are being retrieved.

    Returns:
        Rendered 'user_movies.html' template with the user's movies.
    """
    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/movies', methods=['GET'])
def get_all_movies():
    """
    Route to display all unique movies across users.

    Returns:
        Rendered 'movies.html' template with the list of unique movies.
    """
    users = data_manager.get_all_users()  # Fetch all users
    unique_movies = []  # Initialize an empty list to store unique movies
    movie_set = set()  # Initialize a set to track unique movies

    # Loop through each user and get their favorite movies
    for user in users:
        fav_movies = data_manager.get_user_movies(user.id)  # Fetch movies for the user
        for movie in fav_movies:
            movie_key = (movie.name, movie.director, movie.year)  # Unique identifier for each movie
            if movie_key not in movie_set:  # Check if the movie is already added
                movie_set.add(movie_key)  # Add the movie to the set
                unique_movies.append({
                    "name": movie.name,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating
                })

    return render_template('movies.html', movies=unique_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user.

    Returns:
        Rendered 'add_user.html' template for GET request.
        Redirect to '/users' after adding a user for POST request.
    """
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user(name)
        return redirect('/users')
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/delete', methods=['POST', 'DELETE'])
def delete_user(user_id):
    """
    Route to delete a user by user_id.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
        Redirect to '/users' after deletion.
    """
    data_manager.delete_user(user_id)
    flash(f"User with ID {user_id} has been deleted.", "success")
    return redirect(url_for('get_all_users'))


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route to add a movie to a user's favorites by fetching details from OMDb API.
    """
    user = data_manager.get_user(user_id)

    if request.method == 'POST':
        title = request.form.get('title')

        # Fetch movie details from OMDb API
        movie_data = fetch_movie_details(title)
        if not movie_data:
            flash(f"Movie '{title}' not found in OMDb.", 'error')
            return render_template('add_movie.html', user=user)

        name = movie_data.get('Title')
        director = movie_data.get('Director', 'N/A')
        year = movie_data.get('Year', 0)
        rating = float(movie_data.get('imdbRating', 0))

        if name and year and rating:
            year = int(year) if year.isdigit() else 0
            rating = float(rating) if rating else 0.0
            data_manager.add_movie(user_id=user_id, name=name,
                                   director=director, year=year, rating=rating)
            flash(f'Movie "{name}" added successfully!', 'success')
        else:
            flash('Missing movie details from OMDb. Could not add movie.', 'error')

        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """
    Route to delete a movie from a user's favorites.

    Args:
        user_id (int): ID of the user who owns the movie.
        movie_id (int): ID of the movie to delete.

    Returns:
        Redirect to the user's movie page after deletion.
        :param user_id:
        :param movie_id:
    """
    data_manager.delete_movie(movie_id)
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    """
    Route to add a review to a movie.

    Args:
        user_id (int): ID of the user adding the review.
        movie_id (int): ID of the movie being reviewed.

    Returns:
        Rendered 'add_review.html' template for GET request.
        Redirect to the user's movie page after adding the review for POST request.
    """
    if request.method == 'POST':
        review_text = request.form.get('review_text')

        if not review_text:
            flash('Review cannot be empty.', 'error')
            return redirect(url_for('user_movies', user_id=user_id))

        data_manager.add_review(user_id=user_id, movie_id=movie_id,
                                review_text=review_text)
        flash('Review added successfully.', 'success')
        return redirect(url_for('user_movies', user_id=user_id))

    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_with_reviews(movie_id)

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_review.html', user=user,
                           user_id=user_id, movie=movie, movie_id=movie_id)


@app.route('/users/<int:user_id>/delete_review/<int:review_id>', methods=['POST', 'GET'])
def delete_review(user_id, review_id):
    """
    Route to delete a review by review_id.

    Args:
        user_id (int): ID of the user who posted the review.
        review_id (int): ID of the review to delete.

    Returns:
        Redirect to the user's movie list page after deletion.
    """
    data_manager.delete_review(review_id)
    flash('Review deleted successfully.', 'success')
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found():
    """
    Custom handler for 404 (Page Not Found) errors.

    Returns:
        Rendered '404.html' template and 404 status code.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    """
    Custom handler for 500 (Internal Server Error) errors.

    Returns:
        Rendered '500.html' template and 500 status code.
    """
    return render_template('500.html'), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
