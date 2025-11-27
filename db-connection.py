from flask import Flask, request, jsonify, abort, render_template
from models import db, User, Post
import logging
from datetime import datetime

### Flask App and Database Configuration ###
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
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

### GET Endpoints ###
@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify({
        'status': 'success',
        'message': 'Userss successfully retrieved',
        'data': [user.to_dict() for user in users]
    }), 200

@app.route('/users/<int:student_id>', methods=['GET'])
def get_user(user_id):
    """Get a uers by ID"""
    user = User.query.filter_by(id=user_id)
    return jsonify({
            'status': 'success',
            'message': 'Users successfully retrieved',
            'data': [user.to_dict()]
        }), 200

### POST Endpoints ###
@app.route('/users',methods=['POST'])
def create_user():
    """Create a new user"""
    if not request.json or 'pseudo' not in request.json or 'mail' not in request.json or 'password' not in request.json:
        response_data = {
            'mesage': 'Format invalid or missing values',
            'status': 'error'
            }
        return response_data, 400
    
    user = User(
        pseudo=request.json['pseudo'],
        mail=request.json.get('mail'),
        password=request.json.get('password'),
        role="user"
    )

    try:
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({'status':'error',
                        'message':'User already exists'}), 409
    
    return jsonify({'status':'success',
                    'message':'User successfully created',
                    'data':[user.to_dict()]
                   }), 201

### PUT Endpoints ###
@app.route('/userss/<int:user_id>', methods=['PUT'])
def update_student(user_id):
    """Update the mail an existing user"""
    try:
        user = User.query.get_or_404(user_id)
        if not request.json:
            response_data = {
            'mesage': 'Format invalid or missing values',
            'status': 'error'
            }
            return response_data, 400
        
        user.mail=request.json.get('mail',user.mail)
        db.session.commit()

    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Student does not exist'
        }), 404
    
    return jsonify({'status':'success',
                        'message':'Student successfully modified',
                        'data':[user.to_dict()]
                    }), 200

### DELETE Endpoints ###
@app.route('/users/<int:s=user_id>',methods=['DELETE'])
def delete_user(user_id):
    """Delete an existing user"""
    try:
        user=User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'status':'error',
                        'message':'User does not exist'
                        }), 404
    
    return jsonify({'status':'success',
                    'message':'User successfully deleted'
                   }), 200

if __name__=='__main__':
    app.run(debug=True)