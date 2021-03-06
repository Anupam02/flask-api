import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.cluster import Cluster, ClusterList
from resources.machine import Machine, MachineList
from resources.tag import Tag, TagList


app = Flask(__name__)
app.secret_key = 'anupam'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.route('/home')
def home():
    return {"message":"welcome to default page"}

from db import db
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Cluster, '/cluster/<string:name>')
api.add_resource(Machine, '/machine/<string:name>')
api.add_resource(Tag, '/tag/<string:name>')
api.add_resource(ClusterList, '/clusters')
api.add_resource(MachineList, '/machines')
api.add_resource(TagList, '/tags')
api.add_resource(UserRegister, '/register')

# if __name__ == "__main__":
#     from db import db
#     db.init_app(app)
#     app.run(host='0.0.0.0', port=5000, debug=True)

