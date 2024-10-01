import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from MovieWeb_app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App!" in response.data


def test_list_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b"Users" in response.data  # Assuming "Users" is displayed


def test_user_movies(client):
    # Assuming you have a user with id 1
    response = client.get('/users/1')
    assert response.status_code == 200
    assert b"Favorite Movies" in response.data  # Check if movies section is present


def test_add_user(client):
    response = client.post('/add_user', data={'name': 'Test User'})
    assert response.status_code == 302  # Redirect after adding
    # You can add logic to verify the new user in the database


def test_add_movie(client):
    response = client.post('/users/1/add_movie', data={
        'name': 'Inception',
        'director': 'Christopher Nolan',
        'year': 2010,
        'rating': 9
    })
    assert response.status_code == 302  # Redirect after adding


def test_update_movie(client):
    response = client.post('/users/1/update_movie/1', data={
        'name': 'Inception Updated',
        'director': 'Christopher Nolan',
        'year': 2010,
        'rating': 9
    })
    assert response.status_code == 302  # Redirect after updating


def test_delete_movie(client):
    response = client.post('/users/1/delete_movie/1')
    assert response.status_code == 302  # Redirect after deleting


def test_add_review(client):
    response = client.post('/users/1/movies/1/add_review', data={
        'review_text': 'Amazing movie!'
    })
    assert response.status_code == 302  # Redirect after adding
    # You can also check the database for the new review


def test_delete_review(client):
    response = client.post('/users/1/delete_review/1')
    assert response.status_code == 302  # Redirect after deleting
