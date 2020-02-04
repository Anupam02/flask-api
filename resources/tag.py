from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.tag import TagModel
from models.machine import MachineModel


class Tag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        help='machine name'
                        )
    parser.add_argument('machine_id',
                        type=int,
                        required=True,
                        help='Every tag has to have a machine id.'
                        )

    @jwt_required()
    def get(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            return tag.json()
        return {'message': 'Tag not found'}, 404


    def post(self, name):
        if TagModel.find_by_name(name):
            return {"message": f"An machine with name {name} already exists"}, 400

        data = Tag.parser.parse_args()
        data.update({'name': name})
        tag = TagModel(**data)

        try:
            tag.save_to_db()
        except:
            return {"message": "An error occurred inserting the Tag."}, 500

        return tag.json() , 201

    def put(self, name):
        data = Tag.parser.parse_args()
        tags = TagModel.find_all_by_name(name)
        if not tags:
            return {"message": f"There is no tag name with {name}"}, 400

        for tag in tags:
            machine = MachineModel.query.filter_by(id=tag.id).first()
            machine.delete_from_db()
        
        return {"message": "respective machines has been removed."}



    def delete(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            tag.delete_from_db()

        return {"message": "tag deleted."}


class TagList(Resource):
    def get(self):
        return {'tag': [tag.json() for tag in TagModel.query.all()]}