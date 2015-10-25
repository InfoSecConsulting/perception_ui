from .models import AppUser

# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import PasswordField, StringField, BooleanField, SubmitField

# Import Form validators
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, Email, ValidationError


# Define the login form (WTForms)
class LoginForm(Form):

  username = StringField('Username', [InputRequired(message='Forgot your username?'),
                                      Length(1, 64),
                                      Regexp('^[A-Za-z][A-Za-z0-9!@#$%^&*_.]*$', 0,
                                             'Usernames can not contain () or <>.')])

  password = PasswordField('Password', [InputRequired(message='Must provide a password. ;-)'),
                                        Length(1, 64)])

  password2 = PasswordField('Confirm Password')
  email = StringField('Email')
  firstname = StringField('First Name')
  lastname = StringField('Last Name')
  company = StringField('Company Name')
  phone = StringField('First Name')
  remember_me = BooleanField('Keep me logged in')
  submit = SubmitField('Log In')


class RegistrationForm(Form):

  username = StringField('Username', [InputRequired(message='Forgot your username?'),
                                      Length(1, 64),
                                      Regexp('^[A-Za-z][A-Za-z0-9!@#$%^&*_.]*$', 0,
                                             'Usernames can not contain () or <>.')])

  password = PasswordField('Password', [InputRequired(message='Must provide a password. ;-)'),
                                        Length(1, 64)])

  password2 = PasswordField('Confirm Password')

  email = StringField('Email')

  firstname = StringField('First Name')

  lastname = StringField('Last Name')

  company = StringField('Company Name')

  phone = StringField('First Name')

  submit = SubmitField('Register')

  def validate_email(self, field):
    if AppUser.query.filter_by(email=field.data).first():
      raise ValidationError('Email already registered.')

  def validate_username(self, field):
    if AppUser.query.filter_by(username=field.data).first():
      raise ValidationError('Username already in use.')
