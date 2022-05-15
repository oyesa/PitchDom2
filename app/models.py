from . import login_manager
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model): 
    __tablename__ = 'users' 
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    comments = db.relationship('Comment', backref='author',lazy="dynamic")
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'pitcher',lazy = "dynamic")

    def save_user(self):
            db.session.add(self)
            db.session.commit()

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute') 

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key= True)
    category_name = db.Column(db.String())
    pitches = db.relationship("Pitch", backref ="category", lazy= "dynamic")

    @classmethod
    def get_category_name(cls,category_name):
        categoryName = Category.query.filter_by(category_name = category_name).first()
        return categoryName

    def __repr__(self):
        return f'Category{self.category_name}' 

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.String())
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_comment(self):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_comments(cls,id):
            comments = Comment.query.filter_by(pitch_id=id).all()
            return comments
                
    def __repr__(self):
        return f'COMMENT {self.comment_content}'

class Pitch(db.Model):
        __tablename__ = 'pitches'
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String())
        pitch_content = db.Column(db.String())
        posted = db.Column(db.DateTime,default=datetime.utcnow)
        upvotes = db.Column(db.Integer)
        downvotes = db.Column(db.Integer)
        pitcher_id = db.Column(db.Integer,db.ForeignKey("users.id"))
        category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
        comments = db.relationship("Comment", backref ='pitch', lazy = "dynamic")

        def save_pitch(self):
                db.session.add(self)
                db.session.commit()

        @classmethod
        def get_user_pitch(cls,id):
                user_pitches = Pitch.query.filter_by(pitcher_id = id).order_by(Pitch.posted.desc())
                return user_pitches

        @classmethod
        def get_category_pitch(cls,id):
                category_pitches = Pitch.query.filter_by(category_id = id).order_by(Pitch.posted.desc())
                return category_pitches

        @classmethod
        def get_pitch_id(cls,id):
                pitch_id = Pitch.query.filter_by(id = id).order_by(Pitch.id.desc()) 
                return pitch_id


        def __repr__(self):
                return f"Pitch {self.title}"