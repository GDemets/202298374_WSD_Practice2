from flask import Flask, request, jsonify, abort, render_template
from models import db, Student, Grade
import logging
from datetime import datetime

### Flask App and Database Configuration ###
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

def create_tables():
    db.create_all()

app.before_request(create_tables)
@app.route('/')

### Middleware to log requests ###
@app.before_request
def log_request_info():
    logging.info(f"{datetime.utcnow().isoformat()} - {request.method} {request.path}")

########################################################################################################################
# STUDENT ENDPOINTS
########################################################################################################################
@app.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = Student.query.all()
    return jsonify({
        'status': 'success',
        'message': 'Students successfully retrieved',
        'data': [student.to_dict() for student in students]
    }), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a student by ID"""
    student = Student.query.filter_by(id=student_id)
    return jsonify({
            'status': 'success',
            'message': 'Students successfully retrieved',
            'data': [student.to_dict()]
        }), 200

@app.route('/students',methods=['POST'])
def create_student():
    """Create a new student"""
    
    if not request.json or 'name' not in request.json or 'mail' not in request.json or 'student_number' not in request.json or 'major' not in request.json:
        response_data = {
            'mesage': 'Format invalid or missing values',
            'status': 'error'
            }
        return response_data, 400
    
    student = Student(
        name=request.json['name'],
        student_number=request.json.get('student_number'),
        mail=request.json.get('mail'),
        major=request.json.get('major')
    )

    try:
        db.session.add(student)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({'status':'error',
                        'message':'Student already exists'}), 409
    
    return jsonify({'status':'success',
                    'message':'Student successfully created',
                    'data':[student.to_dict()]
                   }), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update an existing student"""
    try:
        student = Student.query.get_or_404(student_id)
        if not request.json:
            abort(400)
        student.name=request.json.get('name',student.name)
        student.student_number=request.json.get('student_number',student.student_number)
        student.mail=request.json.get('mail',student.mail)
        student.major=request.json.get('major',student.major)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Student does not exist'
        }), 404
    
    return jsonify({'status':'success',
                        'message':'Student successfully modified',
                        'data':[student.to_dict()]
                    }), 200


@app.route('/students/<int:student_id>',methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        student=Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'status':'error',
                        'message':'Student does not exist'
                        }), 404
    
    return jsonify({'status':'success',
                    'message':'Student successfully deleted'
                   }), 200

########################################################################################################################
#### GRADE ENDPOINTS ###
########################################################################################################################
@app.route('/grades', methods=['GET'])
def get_grades():
    """Get all grades"""
    grades = Grade.query.all()
    return jsonify({
        'status': 'success',
        'message': 'Grades successfully retrieved',
        'data': [grade.to_dict() for grade in grades]
    }), 200

@app.route('/professors/<int:grade_id>', methods=['GET'])
def get_grade(grade_id):
    """Get a grade by ID"""
    grade = Grade.query.filter_by(id=grade_id)
    return jsonify({
            'status': 'success',
            'message': 'Grade successfully retrieved',
            'data': [grade.to_dict()]
        }), 200

@app.route('/grades', methods=['POST'])
def create_grade():
    """Create a new grade"""
    
    if not request.json or 'matter' not in request.json or 'average'  not in request.json or 'comment' not in request.json or 'student_id' not in request.json:
        response_data = {
            'mesage': 'Format invalid or missing values',
            'status': 'error'
            }
        return response_data, 400
    
    student = Student.query.get(request.json.get('student_id'))

    if student is None:
        return jsonify({
            'status': 'error',
            'message': 'Student does not exist'
        }), 404
    
    grade = Grade(
        matter=request.json.get('matter'),
        average=request.json.get('average'),
        comment=request.json.get('comment'),
        student_id=request.json.get('student_id')
    )

    try:
        db.session.add(grade)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({'status':'error',
                        'message':'Grade already exists'}), 409
    
    return jsonify({'status':'success',
                    'message':'Grade successfully created',
                    'data':[grade.to_dict()]
                   }), 201

@app.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    """Delete a grade by id"""
    grade = Grade.query.get(grade_id)
    
    if grade is None:
        return jsonify({
            'status': 'error',
            'message': 'Grade not found'
        }), 404
    
    db.session.delete(grade)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Grade successfully deleted'
    }), 200

@app.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    """Update an existing grade by id"""
    grade = Grade.query.get(grade_id)
    
    if grade is None:
        return jsonify({
            'status': 'error',
            'message': 'Grade not found'
        }), 404

    if not request.json:
        return jsonify({
            'status': 'error',
            'message': 'Missing JSON body'
        }), 400

    grade.matter = request.json.get('matter', grade.matter)
    grade.average = request.json.get('average', grade.average)
    grade.comment = request.json.get('comment', grade.comment)

    # Optionnel : mise à jour du student_id
    if request.json.get('student_id'):
        student = Student.query.get(request.json['student_id'])
        if student is None:
            return jsonify({
                'status': 'error',
                'message': 'Student does not exist'
            }), 404
        grade.student_id = request.json['student_id']

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Grade successfully updated',
        'data': grade.to_dict()
    }), 200




if __name__=='__main__':
    app.run(debug=True)