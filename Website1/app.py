from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addresses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set static folder for custom styling
app.static_folder = 'static'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    people = Person.query.all()
    return render_template('list.html', people=people)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    if form.validate_on_submit():
        person = Person(
            name=form.name.data,
            address=form.address.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(person)
        db.session.commit()
        flash('Person added successfully.')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    person = Person.query.get_or_404(id)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        person.name = form.name.data
        person.address = form.address.data
        person.email = form.email.data
        person.phone = form.phone.data
        db.session.commit()
        flash('Person updated successfully.')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)

if __name__ == '__main__':
    os.makedirs(app.static_folder, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
