from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String(30), nullable=False)
    major = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age':self.age,
            'mail':self.mail,
            'major':self.major
        }