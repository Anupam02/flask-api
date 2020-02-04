from db import db

class ClusterModel(db.Model):
    __tablename__ = 'clusters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    cloud_region = db.Column(db.String(40))

    machines = db.relationship('MachineModel', lazy='dynamic')

    def __init__(self, name, cloud_region):
        self.name = name
        self.cloud_region = cloud_region

    def json(self):
        return {'id': self.id, 'name': self.name, 'cloud_region': self.cloud_region, 'machines': [machine.json() for machine in self.machines.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
