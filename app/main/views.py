from crypt import methods
from flask import render_template, redirect, url_for, request, abort, flash
from . import main
from ..models import User, Pitch, Comment, Category
from flask_login import login_required, current_user
from .forms import UpdateProfile, PitchForm, CommentForm, CategoryForm
from .. import db
from ..static import photos

# Views
@main.route('/')
def index():
    title = 'PitchDom'
    categories = Category.query.all()
    return render_template('index.html', title=title, categories=categories) 
    
@main.route('/category/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', category='success')
        return redirect(url_for('.index'))
    return render_template('add_category.html', category_form = form)

@main.route('/pitches/<category_id>')
def pitches_by_category(category_id): 
    pitches = Pitch.get_category_pitch(category_id)
    category = Category.query.filter_by(id = category_id).first()
    category_name = category.category_name
    categories = Category.query.all()
    comments = Comment.query.all()
    title=category_name + " | Pitch"
    return render_template('categories.html', pitches = pitches, categories=categories, category_name=category_name, comments=comments, title=title)

#profile page
@main.route('/user/<uname>', methods=['GET', 'POST'])
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    categories = Category.query.all()
    title = current_user.username + " | Pitch"
    pitches = Pitch.get_user_pitch(user.id)
    return render_template("profile/profile.html", user = user, categories=categories, pitches=pitches, title=title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    categories = Category.query.all()
    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update_profile.html',form =form, categories=categories)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/new-pitch/<uname>', methods=['GET', 'POST'])
@login_required
def new_pitch(uname):
    title = 'New Pitch'
    form = PitchForm()
    user_name = User.query.filter_by(username=uname).first()
    if form.validate_on_submit():
        pitch = form.pitch.data
        category = form.category.data
        new_pitch = Pitch(pitch=pitch,category=category)
        new_pitch.save_pitch()
        return redirect(url_for('main.profile', uname=uname))
    return render_template('create_pitch.html',title=title, pitch_form=form)


@main.route("/comment/<int:pitch_id>", methods=['GET', 'POST'])
@login_required
def new_comment(pitch_id):
    title = 'New Comment'
    form = CommentForm()
    categories = Category.query.all()
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    if form.validate_on_submit():
        comment = Comment(comment_content=form.comment_content.data, author=current_user, pitch_id=pitch_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment was added successfully!', category='success')
        return redirect(url_for('main.pitches_by_category', category_id = pitch.category_id))

    return render_template('add_comment.html', title=title, comment_form=form, categories=categories, pitch=pitch)

@main.route('/upvote_pitch/<pitch_id>')
def upvote (pitch_id):
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    counted_upvotes = pitch.upvotes + 1
    pitch.upvotes = counted_upvotes
    db.session.commit()

    return redirect(url_for('main.pitches_by_category', category_id = pitch.category_id))

@main.route('/downvote_pitch/<pitch_id>')
def downvote (pitch_id):
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    counted_downvotes = pitch.downvotes + 1
    pitch.downvotes = counted_downvotes
    db.session.commit()

    return redirect(url_for('main.pitches_by_category', category_id = pitch.category_id))