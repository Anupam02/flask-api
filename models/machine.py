from db import db

class MachineModel(db.Model):
    __tablename__ = 'machines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    ip_address = db.Column(db.String(15))
    instance_type = db.Column(db.String(20))

    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'))
    cluster = db.relationship('ClusterModel')

    def __init__(self, name, ip_address, instance_type, cluster_id):
        self.name = name
        self.ip_address = ip_address
        self.instance_type = instance_type
        self.cluster_id = cluster_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'ip_address': self.ip_address, 'instance_type': self.instance_type, 'cluster_id': self.cluster_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
