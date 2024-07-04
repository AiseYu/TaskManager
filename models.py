from app import db
from flask_login import UserMixin
class Users(db.Model , UserMixin):

    __tablename__ = 'Users'

    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String , nullable = False)
    password = db.Column(db.String , nullable =False)
    tasks = db.relationship('Tasks' , backref='owner' , lazy=True)

    def __repr__(self):
        return f'<User: {self.username}>'

    def get_id(self):
        return self.uid

class Tasks(db.Model):
    __tablename__ = 'Tasks'

    taskid = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String , nullable = False)
    description = db.Column(db.String , nullable = True)
    isdone = db.Column(db.Boolean , default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable=False)

    def __repr__(self):
        return f'<User: {self.title}>'

    def get_id(self):
        return self.taskid

