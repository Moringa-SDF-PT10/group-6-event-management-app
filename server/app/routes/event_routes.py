from flask import Blueprint, jsonify, request
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt_identity
from app.models.event import Event 
from config import db

event_bp = Blueprint('event_bp', __name__, url_prefix='/events')


# Create new events
@event_bp.route('/', methods=['POST'])
@role_required(['organizer'])
def create_event():
        data = request.get_json()
        organizer_id = get_jwt_identity()
        
        new_event = Event.create(data, organizer_id)
  
        
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

        data = request.get_json()

        for key, value in data.items():
            if hasattr(event, key):
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