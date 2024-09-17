from app.forms import UserLoginForm
from app.models import User, db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

def create_user_from_form(form_data):
    return User(
        email=form_data.get('email'),
        password=form_data.get('password'),
        customer_name=form_data.get('name'),
        age=form_data.get('age'),
        location=form_data.get('location'),
        interests=','.join(form_data.getlist('interests')),
        activity_types=','.join(form_data.getlist('activityTypes')),
        physical_levels=','.join(form_data.getlist('physicalLevel')),
        limitations=form_data.get('limitations'),
        primary_goals=','.join(form_data.getlist('primaryGoal')),
        budget=','.join(form_data.getlist('budget')),
        available_time=form_data.get('available_time')
    )

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = create_user_from_form(request.form)

        try:
            db.session.add(user)
            db.session.commit()

            # Automatically log the user in after successful signup
            login_user(user)
            
            flash(f'Account created successfully, {user.email}! You are now logged in.', 'User-created')
            return redirect(url_for('main.profile'))  # Redirect to profile or main page after login
        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.', 'error')

    return render_template('sign_up.html')


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successful in your initiation. Congratulations, and welcome to unBored app', 'auth-success')
            return redirect(url_for('main.profile'))
        else:
            flash('You do not have access to this content.', 'auth-failed')
            return redirect(url_for('auth.signin'))

    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
