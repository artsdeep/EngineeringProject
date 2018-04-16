from app import db
from app import ma

class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())

class FeatureRequest(db.Model):
    __tablename__ = 'feature_request'
    id = db.Column(db.Integer, db.Sequence('seq_f_request_id', start=1, increment=1), primary_key=True)
    title = db.Column(db.String(128),  nullable=False)
    desc = db.Column(db.String(2000),  nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    #client = db.relationship('Client', backref='rewards')
    client_priority = db.Column(db.Integer, nullable=False)
    date_target = db.Column(db.DateTime, default=db.func.current_timestamp())
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'))

class FeatureRequestSchema(ma.ModelSchema):
    class Meta:
        model = FeatureRequest

class Client(Base):
    __tablename__ = 'client'
    name = db.Column(db.String(128),  nullable=False)

class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client
class ProductArea(Base):
    __tablename__ = 'product_area'
    name = db.Column(db.String(128),  nullable=False)

class ProductAreaSchema(ma.ModelSchema):
    class Meta:
        model = ProductArea

