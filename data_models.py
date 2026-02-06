"""Database models for library management."""
import flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """Author entity with books relationship."""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)
    books = db.relationship('Book', back_populates='author')

class Book(db.Model):
    """Book entity linked to author."""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    isbn = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author = db.relationship('Author', back_populates='books')


