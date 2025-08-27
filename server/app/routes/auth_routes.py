from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity,get_jwt)
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 409
    try:
        new_user = User(username=data['username'], email=data['email'], role=data.get('role', 'attendee'))
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    additional_claims = {"role": new_user.role}
    access_token = create_access_token(identity=str(new_user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(new_user.id))
    return jsonify(access_token=access_token, refresh_token=refresh_token, user=new_user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing username or password'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(access_token=access_token, refresh_token=refresh_token, user=user.to_dict()), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({'message': 'Logout successful.'}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    return jsonify(user.to_dict()) if user else jsonify({'error': 'User not found'}), 404