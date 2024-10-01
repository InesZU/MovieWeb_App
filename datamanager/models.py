from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships
    movies = relationship("Movie", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Movie(Base):
    """
    Represents a movie added by a user.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship("User", back_populates="movies")
    reviews = relationship("Review", back_populates="movie")


class Review(Base):
    """
    Represents a review written by a user for a movie.
    """
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    review_text = Column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
