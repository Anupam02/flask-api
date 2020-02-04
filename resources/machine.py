from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.machine import MachineModel

class Machine(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        help='machine name'
                        )
    parser.add_argument('ip_address',
                        type=str,
                        required=True,
                        help='machine ip address is required.'
                        )
    parser.add_argument('instance_type',
                        type=str,
                        required=True,
                        help='machine instance_type is required.'
                        )
    parser.add_argument('cluster_id',
                        type=int,
                        required=True,
                        help='Every Machine has to have a cluster_id.'
                        )

    @jwt_required()
    def get(self, name):
        machine = MachineModel.find_by_name(name)
        if machine:
            return machine.json()
        return {'message': 'Machine not found'}, 404



    def post(self, name):
        if MachineModel.find_by_name(name):
            return {"message": f"An machine with name {name} already exists"}, 400

        data = Machine.parser.parse_args()
        data.update({'name': name})
        machine = MachineModel(**data)

        try:
            machine.save_to_db()
        except:
            return {"message": "An error occurred inserting the Machine."}, 500

        return machine.json() , 201



    def delete(self, name):
        machine = MachineModel.find_by_name(name)
        if machine:
            machine.delete_from_db()

        return {"message": "machine deleted."}



    def put(self, name):
        data = Machine.parser.parse_args()

        machine = MachineModel.find_by_name(name)

        if machine is None:
            try:
                machine = MachineModel(name, **data)
            except:
                return {"message": "An error occurred while inserting the machine."}, 500
        else:
            try:
                machine.instance_type = data['instance_type']
            except:
                return {"message": "An error occurred updating the machine."}, 500
        machine.save_to_db()

        return machine.json()


class MachineList(Resource):
    def get(self):
        return {'machine': [machine.json() for machine in MachineModel.query.all()]}
