from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), index=True, unique=True)
    requests = db.Column(db.Integer)

    def __init__(self, key, requests):
        self.key = key
        self.requests = requests

    def __repr__(self):
        return '<Key %s, Requests %d>' % (self.key, self.requests)
