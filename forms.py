from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length

#   username = db.Column(db.String(20), primary_key=True, unique = True, nullable = False)
#     password = db.Column(db.Text, nullable = False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     first_name = db.Column(db.Text, nullable = False)
#     last_name = db.Column(db.Text, nullable = False)


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name =StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable = False)
#     username = db.Column(db.String, db.ForeignKey('users.username'))
#     user = db.relationship('User', backref="user_feedback")
class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired(), Length(min=10)])







# class wtforms.validators.Length(min=- 1, max=- 1, message=None)[source]
# Validates the length of a string.

# Parameters
# min – The minimum required length of the string. If not provided, minimum length will not be checked.

# max – The maximum length of the string. If not provided, maximum length will not be checked.

# message – Error message to raise in case of a validation error. Can be interpolated using %(min)d and %(max)d if desired. Useful defaults are provided depending on the existence of min and max.