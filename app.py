"""Flask application for library management system."""
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"
app.secret_key = 'a8f5f167f44f4964e6c998dee827110c'

db.init_app(app)


@app.route('/')
def home():
    """Display all books with their authors."""
    sort_by = request.args.get('sort', 'title')
    search = request.args.get('search', '')

    if search:
        books = Book.query.filter(
            Book.title.ilike(f'%{search}%')
        ).all()
    else:
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()
        else:
            books = Book.query.order_by(Book.title).all()

    return render_template('home.html', books=books, sort_by=sort_by,
                           search=search)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Add new author to database."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birthdate = request.form.get('birthdate', '').strip()
        date_of_death = request.form.get('date_of_death', '').strip()

        if not name:
            flash("Author name is required!", "danger")
            return render_template('add_author.html')

        if not birthdate:
            flash("Birth date is required!", "danger")
            return render_template('add_author.html')

        try:
            birth_dt = datetime.strptime(birthdate, '%Y-%m-%d')
            if birth_dt > datetime.now():
                flash("Birth date cannot be in the future!", "danger")
                return render_template('add_author.html')

            if date_of_death:
                death_dt = datetime.strptime(date_of_death, '%Y-%m-%d')
                if death_dt > datetime.now():
                    flash("Death date cannot be in the future!", "danger")
                    return render_template('add_author.html')
                if death_dt < birth_dt:
                    flash("Death date cannot be before birth date!", "danger")
                    return render_template('add_author.html')
        except ValueError:
            flash("Invalid date format!", "danger")
            return render_template('add_author.html')

        existing = Author.query.filter_by(name=name).first()
        if existing:
            flash("Author already exists!", "danger")
            return render_template('add_author.html')

        try:
            new_author = Author(
                name=name,
                birth_date=birthdate,
                date_of_death=date_of_death if date_of_death else None
            )
            db.session.add(new_author)
            db.session.commit()
            flash(f"Author '{name}' successfully added!", "success")
            return redirect(url_for('home'))
        except Exception:
            db.session.rollback()
            flash("Error saving author to database!", "danger")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add new book to database."""
    if request.method == 'POST':
        isbn = request.form.get('isbn', '').strip()
        title = request.form.get('title', '').strip()
        publication_year = request.form.get('publication_year', '').strip()
        author_id = request.form.get('author', '').strip()

        if not isbn or not title or not author_id:
            flash("All fields are required!", "danger")
            return render_template('add_book.html', authors=Author.query.all())

        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash(f"Book with ISBN {isbn} already exists!", "danger")
            return render_template('add_book.html', authors=Author.query.all())

        try:
            new_book = Book(
                isbn=isbn,
                title=title,
                publication_year=int(publication_year) if publication_year else None,
                author_id=int(author_id)
            )
            db.session.add(new_book)
            db.session.commit()
            flash(f"Book '{title}' successfully added!", "success")
            return redirect(url_for('home'))
        except Exception:
            db.session.rollback()
            flash("Error saving book to database!", "danger")

    return render_template('add_book.html', authors=Author.query.all())


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete book by ID."""
    try:
        book_to_delete = Book.query.get_or_404(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        flash("Book successfully deleted!", "success")
    except Exception:
        db.session.rollback()
        flash("Error deleting book!", "danger")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
