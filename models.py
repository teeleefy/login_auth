from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    '''Connect to our login database.'''
    db.app = app
    db.init_app(app)


# First, create a ***User*** model for SQLAlchemy. Put this in a ***models.py*** file.

# It should have the following columns:

# - ***username*** - a unique primary key that is no longer than 20 characters.
# - ***password*** - a not-nullable column that is text
# - ***email*** - a not-nullable column that is unique and no longer than 50 characters.
# - ***first_name*** - a not-nullable column that is no longer than 30 characters.
# - ***last_name*** - a not-nullable column that is no longer than 30 characters.
    
class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
       """Register user w/hashed password & return user."""
       #protect password by encrypting it with bcrypt
       hashed = bcrypt.generate_password_hash(password)
       #this comes in the form of a bytestring.  Convert it to a normal string (also known as unicode utf8)
       hashed_utf8 = hashed.decode("utf8")
       return cls(username=username, password=hashed_utf8, email=email, first_name = first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        '''Check username and password with database to login user. Return user if successful. Return false if username or password are invalid'''
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

# It’s time to add another model.

# Create a ***Feedback*** model for SQLAlchemy. Put this in a ***models.py*** file.

# It should have the following columns:

# - ***id*** - a unique primary key that is an auto incrementing integer
# - ***title*** - a not-nullable column that is at most 100 characters
# - ***content*** - a not-nullable column that is text
# - ***username*** - a foreign key that references the username column in the users table

class Feedback(db.Model):
    __tablename__ = 'users_feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('User', backref="user_feedback")