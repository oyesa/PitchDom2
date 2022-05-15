from . import login_manager
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash,check_password_hash




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