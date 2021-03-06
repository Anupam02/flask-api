from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    machine = db.relationship('MachineModel')

    def __init__(self, name, machine_id):
        self.name = name
        self.machine_id = machine_id

    def json(self):
        return {'id': self.id, 'name': self.name,  'machine_id': self.machine_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_by_name(cls, name):
        return cls.query.filter_by(name=name)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()