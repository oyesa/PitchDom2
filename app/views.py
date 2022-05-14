from flask import render_template
from app import app

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Welcome to the best pitch website!'
    return render_template('index.html', title = title)

@app.route('/category/<int:add_category_id>')
def add_category(add_category_id):

    '''
    View movie page function that returns the add category details page and its data
    '''
    return render_template('add_category.html',id = add_category_id)