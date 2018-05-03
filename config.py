DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "postgres"
POSTGRES_PW = "artsksks"
POSTGRES_DB = "app"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = DB_URL
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']+"?sslmode=require"
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"