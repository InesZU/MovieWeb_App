from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from .Models import Base, User, Movie, Review
from .DataManager import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    """
    Manages database interactions using SQLite with SQLAlchemy ORM.
    """

    def __init__(self, db_file_name):
        """
        Initializes the SQLiteDataManager with an SQLite database file.
        """
        self.engine = create_engine(f'sqlite:///{db_file_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_user(self, user_id):
        """
        Retrieves a user by their ID.
        """
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        """
        Fetches a user by ID.
        """
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        session = self.Session()
        try:
            return session.query(User).all()
        finally:
            session.close()

    def get_user_movies(self, user_id):
        """
        Retrieves all movies favorite by a specific user.
        """
        session = self.Session()
        try:
            user = session.query(User).options(joinedload(User.movies)
                                               .joinedload(Movie.reviews)).filter_by(id=user_id).first()
            return user.movies if user else []
        finally:
            session.close()

    def get_movie_with_reviews(self, movie_id):
        session = self.Session()
        try:
            # Eagerly load reviews when fetching the movie
            return session.query(Movie).options(joinedload(Movie.reviews)).filter_by(id=movie_id).first()
        finally:
            session.close()

    def get_all_movies(self):
        """
        Fetches all movies in the database.
        """
        session = self.Session()
        try:
            return session.query(Movie).all()
        finally:
            session.close()

    def add_user(self, user_name):
        """
        Adds a new user to the database.
        """
        session = self.Session()
        try:
            new_user = User(name=user_name)
            session.add(new_user)
            session.commit()
        finally:
            session.close()

    def delete_user(self, user_id):
        """
        Deletes a user from the database by ID.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
        finally:
            session.close()

    def get_movie(self, movie_id):
        """
        Retrieves a movie by its ID.
        """
        session = self.Session()
        try:
            return session.query(Movie).filter_by(id=movie_id).first()
        finally:
            session.close()

    def add_movie(self, user_id, name, director, year, rating):
        """
        Adds a movie to a user's list of favorite movies.
        """
        session = self.Session()
        try:
            new_movie = Movie(name=name, director=director, year=year, rating=rating, user_id=user_id)
            session.add(new_movie)
            session.commit()
        finally:
            session.close()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database by ID.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
        finally:
            session.close()

    def add_review(self, user_id, movie_id, review_text):
        """
        Adds a review for a movie by a specific user.
        """
        session = self.Session()
        try:
            new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text)
            session.add(new_review)
            session.commit()
            return new_review
        finally:
            session.close()

    def get_movie_reviews(self, movie_id):
        """
        Fetches all reviews for a specific movie.
        """
        session = self.Session()
        try:
            return session.query(Review).filter_by(movie_id=movie_id).all()
        finally:
            session.close()

    def delete_review(self, review_id):
        """
        Deletes a review from the database by review ID.
        """
        session = self.Session()
        try:
            review = session.query(Review).filter_by(id=review_id).first()
            if review:
                session.delete(review)
                session.commit()
        finally:
            session.close()