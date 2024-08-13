import os
from flask import Flask

# Initialize Flask
app = Flask(__name__)

# Add secret key for authentication
app.secret_key = os.urandom(12)

# Import views
import views


# Initialize database
from model import Auth, Data
D = Data()
A = Auth()
D.create_tables()
A.user_initialize() 

if __name__ == '__main__':
    app.run()