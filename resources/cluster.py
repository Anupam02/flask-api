from flask_restful import Resource, reqparse
from models.cluster import ClusterModel

class Cluster(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        help='cluster name'
                        )
    parser.add_argument('cloud_region',
                        type=str,
                        required=True,
                        help='cloud region is required.'
                        )

    def get(self, name):
        cluster = ClusterModel.find_by_name(name)
        if cluster:
            return cluster.json()
        return {'message': 'Cluster not found'}, 404

    def post(self, name):
        if ClusterModel.find_by_name(name):
            return {"message": f"A cluster with name {name} already exists."}, 400

        data = Cluster.parser.parse_args()
        data.update({'name': name})
        cluster = ClusterModel(**data)
        try:
            cluster.save_to_db()
        except:
            return {"message": "An error occurred while creating the cluster."}, 500
        return cluster.json(), 201

    def delete(self, name):
        cluster = ClusterModel.find_by_name(name)
        if cluster:
            cluster.delete_from_db()

        return {"message": "Cluster deleted."}


class ClusterList(Resource):
    def get(self):
        return {"clusters": [ cluster.json() for cluster in ClusterModel.query.all()]}
