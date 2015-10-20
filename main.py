"""
main python script for perception
(c) copywrite InfoSec Consulting, Inc.
All rights reserverd

"""

from flask import Flask, render_template
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
  return render_template('index.html')

def main():
  index()


if __name__ == '__main__':
  manager.run()
