"""Flask application for library management system."""

import flask

from flask_sqlalchemy import SQLAlchemy
import data_models
import os

#Initialising Flask Server

app = flask.Flask(__name__)


@app.route('/')
def home():
    """Display all books with their authors."""
    return flask.render_template('home.html', books=data_models.Book.query.all())


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Add new author to database."""
    if flask.request.method == 'POST':
        if len(data_models.Author.query.filter_by(name=flask.request.form['name']).all()) == 0:
            new_author_object = data_models.Author(name=flask.request.form['name'],
                            birth_date=flask.request.form['birthdate'],
                            date_of_death=flask.request.form['date_of_death'])
            data_models.db.session.add(new_author_object)
            data_models.db.session.commit()
            flask.flash(f"Author {flask.request.form['name']} successfully added!", "success")

            return flask.redirect(flask.url_for('home'))

        else:
            flask.flash( "Author already exists!", "danger")

    return flask.render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add new book to database."""
    if flask.request.method == 'POST':
        if len(data_models.Author.query.filter_by(isbn=int(flask.request.form['isbn'])).all()) == 0:
            new_book_object = data_models.Book(isbn=flask.request.form['isbn'],
                                           title=flask.request.form['title'],
                                           publication_year=flask.request.form['publication_year'],
                                           author_id=int(flask.request.form['author']))
            data_models.db.session.add(new_book_object)
            data_models.db.session.commit()
            flask.flash( f"Book {flask.request.form['title']} successfully added!", "success")
            return flask.redirect(flask.url_for('home'))

        else:
            flask.flash( f"Book with {flask.request.form['isbn']}  already exist!", "danger")

    return flask.render_template('add_book.html', authors=data_models.Author.query.all())

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """Delete book by ID."""
    book_to_delete = data_models.Book.query.get_or_404(book_id)
    data_models.db.session.delete(book_to_delete)
    data_models.db.session.commit()
    flask.flash( "Book successfully deleted!", "success")
    return flask.redirect(flask.url_for('home'))

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.secret_key = 'a8f5f167f44f4964e6c998dee827110c'

data_models.db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


