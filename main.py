"""
main python script for perception
(c) copywrite InfoSec Consulting, Inc.
All rights reserverd

"""

import lib.yml_parser as parse_yml
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


db_yml = 'config/database.yml'
db_info = parse_yml.db_info(db_yml)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://perceptionsa:perceptionsa@localhost/perception"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/assets')
def assets():
  return render_template('assets.html')


def main():
  index()
  assets()


if __name__ == '__main__':
  manager.run()
