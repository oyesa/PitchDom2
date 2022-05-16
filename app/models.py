from . import login_manager
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime






class User(UserMixin,db.Model): 
    __tablename__ = 'users' 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(50),unique=True, index=True)
    comments = db.relationship('Comment', backref='author',lazy="dynamic")
    bio = db.Column(db.String(150))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(50))
    pitches = db.relationship('Pitch',backref = 'pitcher',lazy = "dynamic")

    #methods to get user information
    @property
    def password(self):
            raise AttributeError('Password is not a readable attribute') 

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.password_hash,password)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @login_manager.user_loader
    def load_user(user_id):
            return User.query.get(int(user_id))

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key= True)
    category_name = db.Column(db.String(50), unique=True)
    pitches = db.relationship("Pitch", backref ="category", lazy= "dynamic")

    @staticmethod
    def get_category_name():
        return Category.query.all()

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Category{self.category_name}' 

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.Text)
    posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
                
#     def __repr__(self):
#         return f'Comment {self.comment_content}'

class Pitch(db.Model):
        __tablename__ = 'pitches'
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String(50))
        pitch_content = db.Column(db.Text)
        posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        upvote = db.relationship('Upvote', backref='post', lazy='dynamic')
        downvote = db.relationship('Downvote', backref='post', lazy='dynamic')
        pitcher_id = db.Column(db.Integer,db.ForeignKey("users.id"))
        category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
        comment = db.relationship("Comment", backref ='pitch', lazy = "dynamic")

        def save_pitch(self):
                db.session.add(self)
                db.session.commit()

        @classmethod
        def get_user_pitch(cls,user_id):
                return cls.query.filter_by(user_id=user_id).order_by(cls.timestamp.desc())

        @classmethod
        def get_category_pitch(cls,category_id):
                return cls.query.filter_by(category_id=category_id).order_by(cls.timestamp.desc())

        @classmethod
        def get_pitch_id(cls,pitch_id): 
                return cls.query.filter_by(pitch_id=pitch_id).order_by(cls.timestamp.desc())


        def __repr__(self):
                return f"Pitch {self.title}"



#upvote and downvote 

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def save_upvote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls, pitch_id):
        upvotes = Upvote.query.filter_by(pitch_id=pitch_id).all()
        return upvotes

    @classmethod
    def get_upvote_author(cls, user_id):
        author = User.query.filter_by(id=user_id).first()
        return author


class Downvote(db.Model):
    __tablename__ = 'downvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls, post_id):
        downvotes = Downvote.query.filter_by(post_id=post_id).all()
        return downvotes

    @classmethod
    def get_downvotes_author(cls, user_id):
        author = User.query.filter_by(id=user_id).first()
        return 