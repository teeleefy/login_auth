#This was an experiment to attempt to separate some of the logic out of my view functions. It did not work.
# from models import User


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

# def register_user(new_user, form, db, IntegrityError, render_template):
#     '''Send new_user made from User model to SQL db'''
#     #access database using SQLalchemy and add new user if possible. Catch error when username is already taken
#     db.session.add(new_user)
#     try:
#         db.session.commit()
#     except IntegrityError:
#         form.username.errors.append('Username taken. Please pick another')
#         return render_template('register.html', form = form)
#     return new_user
    
    
