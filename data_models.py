"""Database models for library management."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Author entity with books relationship."""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)
    books = db.relationship('Book', back_populates='author', lazy=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Book(db.Model):
    """Book entity linked to author."""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"

    def __str__(self):
        return f"{self.title} by {self.author.name if self.author else 'Unknown'}"
