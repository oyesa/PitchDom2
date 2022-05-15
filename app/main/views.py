from flask import render_template, redirect, url_for, request, abort, flash
from . import main
from ..models import User, Pitch, Comment, Category
from flask_login import login_required, current_user
from .forms import UpdateProfile, PitchForm, CommentForm, CategoryForm
from .. import db

# Views
@main.route('/')
def index():
    '''
    View root page function ch returns the index page data
    '''
    title = 'Pitch'
    categories = Category.query.all()
    return render_template('index.html', title=title, categories=categories) 
    
@main.route('/category/add-category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if current_user.username != "Lorna":
        abort(404)
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.index'))

    title = "New Category | Pitch"
    return render_template('add_category.html', category_form = form, title=title)

@main.route('/pitches/<category_id>')
def pitches_by_category(category_id):
    '''
    View pitches page function that displays the pitches available
    '''
    
    pitches = Pitch.get_category_pitch(category_id)
    category = Category.query.filter_by(id = category_id).first()
    category_name = category.category_name
    categories = Category.query.all()
    comments = Comment.query.all()
    title=category_name + " | Pitch"
    return render_template('categories.html', pitches = pitches, categories=categories, category_name=category_name, comments=comments, title=title)
