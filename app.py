from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

from sqlalchemy.exc import IntegrityError
# try:
#     db.session.commit()
# except IntegrityError:
#     form.username.errors.append('Username taken. Please pick another.')



app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

#====================================================================================

#REDIRECT to /register.

@app.route('/')
def direct_to_register():
    '''Redirect to register'''
    return redirect('/register')

#SHOW REGISTER page

@app.route('/register', methods=['GET', 'POST'])
def show_register_page():
    '''Show register page'''
    form = RegisterForm()
    if form.validate_on_submit():
        # new_user_data = get_form_data(form)
        # registered_user = register_user(new_user_data, form)
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        #use User model to put together a new user with form data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another.')
            return render_template('register.html', form = form)
        session['username'] = new_user.username
        flash('Welcome! You Successfully Created Your Account!', "success")
        return redirect(f'/users/{username}')
    
    return render_template('register.html', form=form)

#SHOW LOGIN page

@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    '''Show login page'''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)

#SHARE secret with all users

@app.route('/secrets')
def share_secret():
    '''Original endpoint of logging-in. Showed secret.html'''
    if 'username' not in session:
        flash("Sorry. You don't have access to our secrets. Please register or login to gain access.", "danger")
        return redirect('/register')
    return render_template('secret.html')

#SHOW user profile

@app.route('/users/<username>')
def show_profile(username):
    '''Show user profile'''
    if 'username' not in session:
        flash("Sorry. You are not logged in. Please register or login.", "danger")
        return redirect('/register')
    if session['username'] == username:
        user = User.query.get_or_404(username)
        return render_template('profile.html', user = user)
    flash("Sorry. You don't have access to that account.", "danger")
    return redirect(f"/users/{session['username']}")

#LOGOUT a user

@app.route('/logout')
def logout_user():
    '''Logout a user'''
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')


#DELETE a user

@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_profile(username):
    '''Delete a user'''
    if 'username' not in session:
        flash("Sorry. You are not logged in. Please register or login.", "danger")
        return redirect('/')
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("Account Deleted.", "warning")
        flash("Goodbye!", "info")
        return redirect('/register')
    flash("STOP trying to delete other people's accounts! That's rude.", "danger")
    return redirect(f"/users/{session['username']}")

#ADD a post
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Add a post'''
    if 'username' not in session:
        flash("Sorry. You are not logged in. Please register or login.", "danger")
        return redirect('/')
    if session['username'] == username:
        form = FeedbackForm()
        if form.validate_on_submit():
            user = User.query.get_or_404(username)
            username = username
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title= title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{username}")
        return render_template('/feedback/add_feedback.html', form=form)
    flash("STOP trying to POST using other people's accounts! That's rude.", "danger")
    return redirect(f"/users/{session['username']}")

# DELETE a post

@app.route('/feedback/<int:f_id>/delete', methods=['GET', 'POST'])
def delete_feedback(f_id):
    '''Delete a post'''
    if 'username' not in session:
        flash("Sorry. You are not logged in. Please register or login.", "danger")
        return redirect('/')
    feedback = Feedback.query.get_or_404(f_id)
    current_user = session['username']
    if current_user == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback Deleted.", "warning")
        return redirect(f'/users/{current_user}')
    flash("STOP trying to delete other people's posts! That's rude.", "danger")
    return redirect(f"/users/{session['username']}")

#UPDATE a post

@app.route('/feedback/<int:f_id>/update', methods=['GET', 'POST'])
def update_feedback(f_id):
    '''Update a post'''
    if 'username' not in session:
        flash("Sorry. You are not logged in. Please register or login.", "danger")
        return redirect('/')
    feedback = Feedback.query.get_or_404(f_id)
    current_user = session['username']
    if current_user == feedback.username:
        form = FeedbackForm()
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            flash("Updated feedback.", "success")
            return redirect(f"/users/{current_user}")
        return render_template('/feedback/update_feedback.html', form=form, feedback=feedback)
    flash("STOP trying to MESS WITH other people's posts! That's rude.", "danger")
    return redirect(f"/users/{session['username']}")



#===================================================================
#THIS WAS ANOTHER EXPERIMENT TO SEPARATE DATA OUT OF MY VIEW FUNCTIONS
# def get_form_data(form):
#     '''Register new user by accessing form data'''
#     #get form data
#     username = form.username.data
#     password = form.password.data
#     email = form.email.data
#     first_name = form.first_name.data
#     last_name = form.last_name.data
#     #use User model to put together a new user with form data
#     new_user = User.register(username, password, email, first_name, last_name)
#     return new_user

# def register_user(new_user, form):
#     '''Send new_user made from User model to SQL db'''
#     #access database using SQLalchemy and add new user if possible. Catch error when username is already taken
#     db.session.add(new_user)
#     try:
#         db.session.commit()
#     except IntegrityError:
#         form.username.errors.append('Username taken. Please pick another')
#         return render_template('register.html', form = form)
#     return new_user
    
#===============================================================================




