from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from app import login_manager


class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
  updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class AppUser(UserMixin, Base):
  __tablename__ = 'app_users'

  username = db.Column(db.String(128), nullable=False, unique=True)
  firstname = db.Column(db.String(128))
  lastname = db.Column(db.String(128))
  email = db.Column(db.String(128), nullable=False)
  phone = db.Column(db.VARCHAR(12))
  company = db.Column(db.String(32))
  password_hash = db.Column(db.String(255), nullable=False)

  def __init__(self, username, email, password, firstname, lastname,company, phone):
    self.username = username.lower()
    self.email = email.lower()
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.company = company
    self.phone = phone
    self.set_password(password)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(app_users_id):
  return AppUser.query.get(int(app_users_id))
