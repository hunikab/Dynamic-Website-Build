"""
Restaurant Menu Management Flask Application

This application provides a web interface for restaurant menu management,
including viewing menu items, adding new items, editing existing items,
and processing customer orders through a checkout system.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.static_folder = 'static'
db = SQLAlchemy(app)


class MenuItem(db.Model):
    """
    Database model for menu items.
    
    Attributes:
        id: Unique identifier for the menu item
        type: Category or type of the menu item
        description: Detailed description of the menu item
        cost: Price of the menu item in KES
    """
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)


class MenuItemForm(FlaskForm):
    """
    Form for creating and editing menu items.
    
    Fields:
        type: Category or type of the menu item
        description: Detailed description of the menu item
        cost: Price of the menu item in AUD
        submit: Form submission button
    """
    
    type = StringField('Item Type', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    cost = DecimalField('Cost (AUD)', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    """
    Homepage route that displays all menu items.
    
    Returns:
        Rendered template showing all menu items
    """
    items = MenuItem.query.all()
    return render_template('menu_list.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Route for adding new menu items.
    
    GET: Displays the form for adding a new menu item
    POST: Processes the form submission and adds the new item to the database
    
    Returns:
        Rendered add item form template or redirects to index page after successful
        form submission
    """
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(
            type=form.type.data,
            description=form.description.data,
            cost=float(form.cost.data)
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added to menu!')
        return redirect(url_for('index'))
    return render_template('add_item.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    """
    Route for editing existing menu items.
    
    Args:
        id: The ID of the menu item to edit
    
    GET: Displays the form with current item details for editing
    POST: Processes the form submission and updates the item in the database
    
    Returns:
        Rendered edit item form template or redirects to index page after successful
        form submission
    """
    item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=item)
    if form.validate_on_submit():
        item.type = form.type.data
        item.description = form.description.data
        item.cost = float(form.cost.data)
        db.session.commit()
        flash('Item updated!')
        return redirect(url_for('index'))
    return render_template('edit_item.html', form=form)


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Route for processing customer orders and checkout.
    
    Receives selected menu items from the form submission,
    calculates the total cost, and displays the order summary.
    
    Returns:
        Rendered checkout template with selected items and total cost
    """
    selected_ids = request.form.getlist('selected_items')
    selected_items = MenuItem.query.filter(MenuItem.id.in_(selected_ids)).all()
    total = sum(item.cost for item in selected_items)
    return render_template('checkout.html', items=selected_items, total=total)


if __name__ == '__main__':
    """
    Application entry point for direct execution.
    Creates static folder, ensures database tables exist, and starts the Flask server.
    """
    os.makedirs(app.static_folder, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

