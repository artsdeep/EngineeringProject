# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)

# Configurations
#app.config.from_object('config')
POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "app_user"
POSTGRES_PW = "app_user_pass"
POSTGRES_DB = "app"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)


SQLALCHEMY_DATABASE_URI = DB_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)
from app.request.models import *

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.request.controllers import feature_request

app.register_blueprint(feature_request)

db.create_all()

from app.request.models import Client
# Import flask and template operators
from flask import Flask, render_template

path_sql_script = os.path.abspath(os.path.dirname(__file__))
print(path_sql_script)
if db.session.query(Client).count() == 0:
    sql_command = ''
    sql_file = open(path_sql_script+"/app/db.sql", 'r')
    for line in sql_file:
        if not line.startswith('--') and line.strip('\n'):
            sql_command += line.strip('\n')
            if sql_command.endswith(';'):
                try:
                    db.engine.execute(str(sql_command))

                    # Assert in case of error
                except:
                    print('Ops')

                finally:
                    sql_command = ''