from re import compile, sub
from os import path

# Define the database - we are working with
db_yml = 'app/config/database.yml'
new_list = []
reg_clean = compile(r'[:]')
with open(db_yml, 'r') as f:
  new_list += [sub(r':\s', ':', line.strip()) for line in f if reg_clean.search(line)]
  db_info = dict(map(str, x.split(':')) for x in new_list)

# build URL
# driver://user:pass@localhost/dbname
sqlalchemy_url = '%s://%s:%s@%s/%s' % (db_info['drivername'],
                                       db_info['username'],
                                       db_info['password'],
                                       db_info['host'],
                                       db_info['database'])

class Config:

  # Statement for enabling the development environment
  DEBUG = True

  # Define the application directory
  BASE_DIR = path.abspath(path.dirname(__file__))

  SQLALCHEMY_DATABASE_URI = sqlalchemy_url
  DATABASE_CONNECT_OPTIONS = {}

  # Application threads. A common general assumption is
  # using 2 per available processor cores - to handle
  # incoming requests using one and performing background
  # operations using the other.
  THREADS_PER_PAGE = 2

  # Enable protection agains *Cross-site Request Forgery (CSRF)*
  CSRF_ENABLED = True

  # Use a secure, unique and absolutely secret key for
  # signing the data.
  CSRF_SESSION_KEY = "secret"

  # Secret key for signing cookies
  SECRET_KEY = "secret"
  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = sqlalchemy_url

config = {
    'development': DevelopmentConfig,
    #'testing': TestingConfig,
    #'production': ProductionConfig,
    #'heroku': HerokuConfig,
    #'unix': UnixConfig,

    'default': DevelopmentConfig
}
