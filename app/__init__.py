# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.request.controllers import feature_request

app.register_blueprint(feature_request)

new_db = db.create_all()
from app.request.models import Client
if db.session.query(Client).count() == 0:
    db.engine.execute("insert into client(id, name) values (1, 'Client A')")
    db.engine.execute("insert into client(id, name) values (2, 'Client B')")
    db.engine.execute("insert into client(id, name) values (3, 'Client C')")
    db.engine.execute("insert into product_area(id, name) values (1, 'Policies')")
    db.engine.execute("insert into product_area(id, name) values (2, 'Billing')")
    db.engine.execute("insert into product_area(id, name) values (3, 'Claims')")
    db.engine.execute("insert into product_area(id, name) values (4, 'Reports')")