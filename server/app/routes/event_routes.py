from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app import db
from app.models import Event, Category
from flask_jwt_extended import jwt_required, get_jwt_identity

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

@event_bp.route('', methods=['GET'])
def get_events():
    #Get all events with optional search and filtering
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page

        # Start with base query
        query = Event.query

        # Apply search filter (search in title and description)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Event.title.ilike(search_term),
                    Event.description.ilike(search_term)
                )
            )

        # Apply category filter
        if category:
            query = query.join(Event.categories).filter(Category.name.ilike(f"%{category}%"))

        # Order by date (upcoming events first)
        query = query.order_by(Event.date.asc())

        # Paginate results
        paginated_events = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Serialize events
        events_data = []
        for event in paginated_events.items:
            events_data.append(event.to_dict())

        return jsonify({
            'events': events_data,
            'pagination': {
                'page': page,
                'pages': paginated_events.pages,
                'per_page': per_page,
                'total': paginated_events.total,
                'has_next': paginated_events.has_next,
                'has_prev': paginated_events.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    #Get a single event by ID
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify({
            'event': event.to_dict(include_organizer=True, include_categories=True)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@event_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    #Create a new event (organizers only)
    try:
        current_user_id = get_jwt_identity()
        
        # Get current user to check role
        from app.models import User
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'organizer':
            return jsonify({'error': 'Only organizers can create events'}), 403

        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'date', 'location', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Create new event
        event = Event(
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            price=float(data['price']),
            image_url=data.get('image_url'),
            organizer_id=current_user_id
        )

        # Add categories if provided
        if 'category_ids' in data:
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            event.categories = categories

        db.session.add(event)
        db.session.commit()

        return jsonify({
            'message': 'Event created successfully',
            'event': event.to_dict()
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@event_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    #Update an event (only by its organizer)
    try:
        current_user_id = get_jwt_identity()
        event = Event.query.get_or_404(event_id)

        # Check if current user is the organizer
        if event.organizer_id != current_user_id:
            return jsonify({'error': 'You can only update your own events'}), 403

        data = request.get_json()

        # Update fields if provided
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = data['date']
        if 'location' in data:
            event.location = data['location']
        if 'price' in data:
            event.price = float(data['price'])
        if 'image_url' in data:
            event.image_url = data['image_url']

        # Update categories if provided
        if 'category_ids' in data:
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            event.categories = categories

        db.session.commit()

        return jsonify({
            'message': 'Event updated successfully',
            'event': event.to_dict()
        }), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@event_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    #Delete an event (only by its organizer
    try:
        current_user_id = get_jwt_identity()
        event = Event.query.get_or_404(event_id)

        # Check if current user is the organizer
        if event.organizer_id != current_user_id:
            return jsonify({'error': 'You can only delete your own events'}), 403

        db.session.delete(event)
        db.session.commit()

        return jsonify({'message': 'Event deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500