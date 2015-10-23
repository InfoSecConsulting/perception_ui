# Import flask dependencies
from flask import request, render_template, flash, session, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import module forms
from .forms import LoginForm, RegistrationForm
from .models import AppUser
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
# auth = Blueprint('auth', __name__, url_prefix='/auth')
from . import auth

# Set the route and accepted methods
@auth.route('/login', methods=['GET', 'POST'])
def login():

  # If sign in form is submitted

  form = LoginForm(request.form)

  if request.method == 'POST':

    # Verify the sign in form
    if form.validate_on_submit():
      user = AppUser.query.filter_by(username=form.username.data).first()
      if user and check_password_hash(user.password_hash, form.password.data):
        session['username'] = form.username.data
        login_user(user, form.remember_me.data)
        flash('Welcome %s' % user.username)
        return redirect(url_for('index'))
      flash('Wrong username or password', 'error-message')

  return render_template("auth/login.html", form=form)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You are now logged out')
  return redirect(url_for('index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():

  form = RegistrationForm()

  if request.method == 'POST':

    if form.validate_on_submit():
      user = AppUser(username=form.username.data,
                     password=form.password.data,
                     email=form.email.data,
                     firstname=form.firstname.data,
                     lastname=form.lastname.data,
                     phone=form.phone.data,
                     company=form.company.data)
      try:
        db.session.add(user)
        db.session.commit()
      except IntegrityError as e:
        db.session.rollback()
        flash('Some thing went horribly wrong, try again.', e)
        return redirect(url_for('auth.login'))
      flash('You are now registered')
      session['username'] = form.username.data
      login_user(user)
      flash('Welcome %s' % user.username)
      return redirect(url_for('index'))

  return render_template("auth/login.html", form=form)
