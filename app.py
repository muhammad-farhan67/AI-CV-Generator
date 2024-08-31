import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import re
import logging
from functools import lru_cache

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

logging.basicConfig(level=logging.INFO)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_data = db.Column(db.Text, nullable=True)

def validate_input(data):
    if not data.get('username') or not data.get('password'):
        return False, "Username and password are required"
    if len(data['password']) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email', '')):
        return False, "Invalid email format"
    return True, ""

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        is_valid, message = validate_input(data)
        if not is_valid:
            return jsonify({"error": message}), 400
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_password, email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        logging.info(f"New user registered: {data['username']}")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logging.error(f"Error in user registration: {str(e)}")
        return jsonify({"error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.username)
            logging.info(f"User logged in: {data['username']}")
            return jsonify({"access_token": access_token}), 200
        logging.warning(f"Failed login attempt for user: {data['username']}")
        return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Error in user login: {str(e)}")
        return jsonify({"error": "Login failed"}), 500

@app.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        data = request.json
        user = User.query.filter_by(username=get_jwt_identity()).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if 'email' in data:
            user.email = data['email']
        if 'user_data' in data:
            user.user_data = data['user_data']
        
        db.session.commit()
        logging.info(f"Profile updated for user: {user.username}")
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error in profile update: {str(e)}")
        return jsonify({"error": "Profile update failed"}), 500

@lru_cache(maxsize=100)
def get_job_match(job_description, user_data):
    # Simplified job matching logic
    common_words = set(job_description.lower().split()) & set(user_data.lower().split())
    match_score = len(common_words) / (len(set(job_description.split())) + len(set(user_data.split())))
    return match_score

@app.route('/generate_cv', methods=['POST'])
@jwt_required()
def generate_cv():
    try:
        data = request.json
        job_description = data['job_description']
        user = User.query.filter_by(username=get_jwt_identity()).first()
        user_data = user.user_data if user else ""
        
        match_score = get_job_match(job_description, user_data)
        
        cv = f"Generated CV based on:\nJob Description: {job_description}\nUser Data: {user_data}\nMatch Score: {match_score:.2f}"
        
        logging.info(f"CV generated for user: {user.username}")
        return jsonify({"cv": cv, "match_score": match_score})
    except Exception as e:
        logging.error(f"Error in CV generation: {str(e)}")
        return jsonify({"error": "CV generation failed"}), 500

@app.route('/generate_cover_letter', methods=['POST'])
@jwt_required()
def generate_cover_letter():
    try:
        data = request.json
        job_description = data['job_description']
        user = User.query.filter_by(username=get_jwt_identity()).first()
        user_data = user.user_data if user else ""
        
        match_score = get_job_match(job_description, user_data)
        
        cover_letter = f"Generated Cover Letter based on:\nJob Description: {job_description}\nUser Data: {user_data}\nMatch Score: {match_score:.2f}"
        
        logging.info(f"Cover letter generated for user: {user.username}")
        return jsonify({"cover_letter": cover_letter, "match_score": match_score})
    except Exception as e:
        logging.error(f"Error in cover letter generation: {str(e)}")
        return jsonify({"error": "Cover letter generation failed"}), 500

@app.route('/prepare_interview', methods=['POST'])
@jwt_required()
def prepare_interview():
    try:
        data = request.json
        job_description = data['job_description']
        user = User.query.filter_by(username=get_jwt_identity()).first()
        user_data = user.user_data if user else ""
        
        match_score = get_job_match(job_description, user_data)
        
        interview_questions = f"Generated Interview Questions based on:\nJob Description: {job_description}\nUser Data: {user_data}\nMatch Score: {match_score:.2f}"
        
        logging.info(f"Interview questions generated for user: {user.username}")
        return jsonify({"interview_questions": interview_questions, "match_score": match_score})
    except Exception as e:
        logging.error(f"Error in interview preparation: {str(e)}")
        return jsonify({"error": "Interview preparation failed"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
