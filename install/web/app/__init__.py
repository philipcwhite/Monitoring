from flask import Flask
import os

# Initialize Flask
app = Flask(__name__, instance_relative_config=True)

# Add secret key for authentication
app.secret_key = os.urandom(12)

# Import views
from app import views

# Load Flask Configuration (instance/flask.cfg)
app.config.from_pyfile('flask.cfg')

# Initialize database
from .model import Auth, Data
D = Data()
A = Auth()
A.user_initialize() 