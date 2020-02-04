import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.cluster import Cluster, ClusterList
from resources.machine import Machine, MachineList


app = Flask(__name__)
app.secret_key = 'anupam'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Cluster, '/cluster/<string:name>')
api.add_resource(Machine, '/machine/<string:name>')
api.add_resource(ClusterList, '/clusters')
api.add_resource(MachineList, '/machines')
api.add_resource(UserRegister, '/register')

