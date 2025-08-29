from flask import Blueprint, jsonify, request, current_app
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt_identity
from app.models.event import Event 
from app import db
import os
import uuid
from werkzeug.utils import secure_filename


event_bp = Blueprint('event_bp', __name__, url_prefix='/events')


# Create new events
@event_bp.route('/', methods=['POST'])
@role_required(['organizer'])
def create_event():
    if 'banner_image' in request.files:
        file = request.files['banner_image']
        if file:
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            banner_image_url = f"/uploads/{filename}" 

        data = request.form.to_dict()
    else:
        data = request.get_json()
        banner_image_url = data.get('banner_image_url')

        organizer_id = get_jwt_identity()
    
        new_event_data = {
        'name': data.get('name'),
        'description': data.get('description'),
        'date': data.get('date'),
        'price': data.get('price'),
        'capacity': data.get('capacity'),
        'banner_image_url': banner_image_url
    }
    
    new_event = Event.create(new_event_data, organizer_id)
    
    return jsonify({
        'message': 'Event created successfully',
        'event_id': new_event.id,
        'event_data': new_event.to_dict()
    }), 201

# Edit events
@event_bp.route('/<int:id>', methods=['PATCH'])
@role_required(['organizer'])
def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
        
    organizer_id = get_jwt_identity()
    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Unauthorized to update this event'}), 403

    if 'banner_image' in request.files:
        file = request.files['banner_image']
        if file:
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            event.banner_image_url = f"/uploads/{filename}"
        
        data = request.form.to_dict()
    else:
        data = request.get_json()
        if 'banner_image_url' in data:
            event.banner_image_url = data['banner_image_url']
            
    for key, value in data.items():
        if hasattr(event, key) and key != 'banner_image_url':
            setattr(event, key, value)
            
    db.session.commit()
    
    return jsonify({
        'message': 'Event updated successfully',
        'event': event.to_dict()
    }), 200


# Delete events
@event_bp.route('/<int:id>', methods=['DELETE'])
@role_required(['organizer'])
def delete_event(id):      
        event = Event.query.get(id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        organizer_id = get_jwt_identity()

        if event.organizer_id != organizer_id:
            return jsonify({'error': 'Unauthorized to delete this event'}), 403

        db.session.delete(event)

        db.session.commit()
        
        return jsonify({
            'message': 'Event deleted successfully'
        }), 200