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

  logon_form = LoginForm(request.form)

  if request.method == 'POST':

    # Verify the sign in form
    if logon_form.validate_on_submit():
      user = AppUser.query.filter_by(username=logon_form.username.data).first()
      if user and check_password_hash(user.password_hash, logon_form.password.data):
        session['username'] = logon_form.username.data
        login_user(user, logon_form.remember_me.data)
        flash('Welcome %s' % user.username)
        return redirect(url_for('dashboards.overview'))
      flash('Wrong username or password', 'error-message')

  return render_template("auth/login.html",
                         logon_form=logon_form,
                         reg_form=RegistrationForm)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You are now logged out')
  return redirect(url_for('dashboards.overview'))

@auth.route('/register', methods=['GET', 'POST'])
def register():

  reg_form = RegistrationForm(request.form)

  if request.method == 'POST':

    if reg_form.validate_on_submit():
      user = AppUser(username=reg_form.username.data,
                     password=reg_form.password.data,
                     email=reg_form.email.data,
                     firstname=reg_form.firstname.data,
                     lastname=reg_form.lastname.data,
                     phone=reg_form.phone.data,
                     company=reg_form.company.data)
      try:
        db.session.add(user)
        db.session.commit()
      except IntegrityError as e:
        db.session.rollback()
        flash('Some thing went horribly wrong, try again.', e)
        return redirect(url_for('auth.login'))
      flash('You are now registered')
      session['username'] = reg_form.username.data
      login_user(user)
      flash('Welcome %s' % user.username)
      return redirect(url_for('dashboards.overview'))

  return render_template("auth/login.html",
                         reg_form=reg_form,
                         logon_form=LoginForm)
