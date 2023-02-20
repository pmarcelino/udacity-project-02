import os

SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost:5432/trivia"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(32)