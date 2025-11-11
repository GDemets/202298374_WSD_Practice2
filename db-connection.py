from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullabe=False)
    age = db.Column(db.Integer, nullabe=False)
    mail = db.Column(db.String, nullabe=False)
    major = db.Column(db.String,nullabe=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age':self.age,
            'mail':self.mail,
            'major':self.major
        }