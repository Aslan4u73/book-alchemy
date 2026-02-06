import flask

from flask_sqlalchemy import SQLAlchemy
import data_models
import os

#Initialising Flask Server
app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if flask.request.method == 'POST':
        new_author_object = data_models.Author(name=flask.request.form['name'],
                            birth_date=flask.request.form['birthdate'],
                            date_of_death=flask.request.form['date_of_death'])

        data_models.db.session.add(new_author_object)
        data_models.db.session.commit()
        return f"Author {flask.request.form['name']} successfully added!"
    else:
        return flask.render_template('add_author.html')



basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

data_models.db.init_app(app)
app.run(debug=True, host='0.0.0.0', port=8080)