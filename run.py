import os
from flask.ext.script import Manager
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Run a test server.
#from app import app
#from flask.ext.script import Manager

manager = Manager(app)

#app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
  manager.run()
