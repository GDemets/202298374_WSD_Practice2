from flask import Flask, request, jsonify, abort
from models import db, Student

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

def create_tables():
    db.create_all()

app.before_request(create_tables)

@app.route('/students',methodes=['GET'])
def get_students():
    students=Student.query.all()
    return jsonify([student.to_dict for student in students])