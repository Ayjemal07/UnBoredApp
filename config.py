#This file hols configuration settings

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for flask session management
    SECRET_KEY = os.getenv('FLASK_SESSION')

    # Other API keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


        # Set session timeout (example: 30 minutes)
    PERMANENT_SESSION_LIFETIME = 300  # 1800 seconds = 30 minutes, do 1 min for now(for testing)
