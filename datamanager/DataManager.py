from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Interface that defines the required methods for managing users, movies, and reviews.
    Classes that implement this interface are responsible for interacting with a specific data source.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieve all users from the data source.

        Returns:
            A list of all users.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieve all movies favorited by a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            A list of movies for the specified user.
        """
        pass

    @abstractmethod
    def get_all_movies(self):
        """
        Retrieve all unique movies from the data source.

        Returns:
            A list of all unique movies.
        """
        pass

    @abstractmethod
    def add_user(self, name):
        """
        Add a new user to the data source.

        Args:
            name (str): The name of the new user.
        """
        pass

    @abstractmethod
    def add_movie(self, user_id, name, director, year, rating):
        """
        Add a movie to a user's favorite list.

        Args:
            user_id (int): The ID of the user adding the movie.
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (int): The year the movie was released.
            rating (int): The user's rating of the movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Remove a movie from the data source.

        Args:
            movie_id (int): The ID of the movie to delete.
        """
        pass

    @abstractmethod
    def add_review(self, user_id, movie_id, review_text):
        """
        Add a review to a specific movie.

        Args:
            user_id (int): The ID of the user adding the review.
            movie_id (int): The ID of the movie being reviewed.
            review_text (str): The text content of the review.
        """
        pass

    @abstractmethod
    def get_movie_reviews(self, movie_id):
        """
        Retrieve all reviews for a specific movie.

        Args:
            movie_id (int): The ID of the movie for which reviews are fetched.

        Returns:
            A list of reviews for the specified movie.
        """
        pass

    @abstractmethod
    def delete_review(self, review_id):
        """
        Delete a review from the data source.

        Args:
            review_id (int): The ID of the review to delete.
        """
        pass
