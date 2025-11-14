from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    mail = db.Column(db.String(30), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    grade=db.relationship('Grade', backref='student', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_number':self.student_number,
            'mail':self.mail,
            'major':self.major
        }

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matter = db.Column(db.String(30), nullable=False)
    average = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(30), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'matter': self.matter,
            'average':self.average,
            'comment': self.comment,
            'student_id':self.student_id
        }