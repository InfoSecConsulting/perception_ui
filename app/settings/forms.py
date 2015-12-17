# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import PasswordField, StringField, BooleanField, SubmitField

# Import Form validators
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, Email, ValidationError


# Define the login form (WTForms)
class Seeds(Form):
  ip_addr = StringField('Core Router')
  username = StringField('Username')
  password = PasswordField('Password')
  enable_password = PasswordField('Enable Password')
  #snmp_string_ro = PasswordField('SNMP String RO')
  #snmp_string_rw = PasswordField('SNMP String RW')
  #snmp_user = StringField('SNMP User')
  #snmp_group = StringField('SNMP Group')
  submit = SubmitField('Submit')

class ServiceAccounts(Form):
  username = StringField('Username')
  password = PasswordField('Password')
  enable_password = PasswordField('Enable Password')
  submit = SubmitField('Submit')
  radio2 = StringField('radio2')
  #smb_user = BooleanField('smb_user')
  domain_name = StringField('Domain Name')
  description = StringField('Description')
