# Import flask dependencies
import datetime
from flask import Blueprint, request, render_template, jsonify
from app.request.models import Client, ClientSchema, FeatureRequest, ProductArea, FeatureRequestSchema, ProductAreaSchema, db
from flask import send_from_directory
import os
import app
feature_request = Blueprint('auth', __name__, url_prefix='/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@feature_request.route('', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@feature_request.route('get_default_request', methods=['POST'])
def get_default_request():
    f_request = FeatureRequest.query.all()
    f_request_schema = FeatureRequestSchema(many=True)
    output = f_request_schema.dump(f_request).data
    return jsonify({'request': output})
@feature_request.route('get_clients', methods=['POST'])
def get_clients():
    dd = app
    clients = Client.query.order_by(Client.name).all()
    client_schema = ClientSchema(many=True)
    output = client_schema.dump(clients).data
    return jsonify({'clients': output})
@feature_request.route('get_product_areas', methods=['POST'])
def get_product_areas():
    productAreas = ProductArea.query.order_by(ProductArea.name).all()
    product_area_schema = ProductAreaSchema(many=True)
    output = product_area_schema.dump(productAreas).data
    return jsonify({'productAreas': output})
@feature_request.route('add_feature_request', methods=['POST'])
def add_feature_request():
    content = request.get_json(silent=True)
    try:
        priority = int(content["clientPriority"])
        db.engine.execute("update feature_request set client_priority = client_priority+1 where client_priority >= "+str(priority))
    except:
        return jsonify({'status': 'bad'})
    f_request = FeatureRequest(title=content["title"], desc=content["desc"], client_id=content["clientValue"], client_priority=content["clientPriority"], date_target=datetime.datetime.strptime(content["targetDate"], '%Y-%m-%dT%H:%M:%S.%fZ'))
    db.session.add(f_request)
    db.session.commit()

    return jsonify({'status': 'good'})
