#Models are used for creating classes that are used repeatedly 
# to populate databases.

# Import db from __init__.py
# from . import db

#UUID stands for universally unique identifiers. 
#These are great for creating independent items that won't clash with other items
import uuid 

#imports date and time
from datetime import datetime


#Werkzeug is a security package. This allows us to make the password data that we store in our 
#database secret, so that if we log in to look at our database, 
#we can't see what users saved as their password!
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
from flask_sqlalchemy import SQLAlchemy

import secrets

db = SQLAlchemy()

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # default_duration=db.Column(db.Integer,nullable=True)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    why_worth = db.Column(db.String(500), nullable=False)
    youtube_link = db.Column(db.String(500), nullable=False)
    meetup_link = db.Column(db.String(500), nullable=False)
    google_link = db.Column(db.String(500), nullable=False)
    cherry_picked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Activity {self.name}>'
    

    def serialize(self):
        # Define serialization logic
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'why_worth': self.why_worth,
            'google_link':self.google_link,
            'youtube_link':self.youtube_link,
            'meetup_link':self.meetup_link,
            'cherry_picked': self.cherry_picked
        }