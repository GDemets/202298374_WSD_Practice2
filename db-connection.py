from flask import Flask, request, jsonify, abort, render_template
from models import db, Student

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

def create_tables():
    db.create_all()

app.before_request(create_tables)

@app.route('/')
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    students = Student.query.filter_by(id=student_id)
    return jsonify([student.to_dict() for student in students])

@app.route('/students',methods=['POST'])
def create_student():
    if not request.json or not 'name' in request.json:
        abort(400)
    
    student = Student(
        name=request.json['name'],
        age=request.json.get('age'),
        mail=request.json.get('mail'),
        major=request.json.get('major')
    )

    try:
        db.session.add(student)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({'error': 'Student already exists!'}), 409
    
    return jsonify(student.to_dict()), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        if not request.json:
            abort(400)
        student.name=request.json.get('name',student.name)
        student.age=request.json.get('age',student.age)
        student.mail=request.json.get('mail',student.mail)
        student.majour=request.json.get('major',student.major)

        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error':'Student does not exist'}), 404
    
    return jsonify(student.to_dict()), 200

@app.route('/students/<int:student_id>',methods=['DELETE'])
def delete_student(student_id):
    try:
        student=Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error':'Student does not exist'}), 404
    
    return jsonify({'result':True,'message': f'Student {student_id} deleted'})


if __name__=='__main__':
    app.run(debug=True)