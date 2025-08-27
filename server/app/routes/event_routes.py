from flask import Blueprint, jsonify, request
from app import db
from app.models.event import Event
from app.models.category import Category
from sqlalchemy import or_, and_
from datetime import datetime

event_bp = Blueprint('events', __name__)

@event_bp.route('/events', methods=['GET'])
def get_events():
    
    try:
        # Base query - only active events
        query = Event.query.filter_by(is_active=True)
        
        # Search functionality
        search_term = request.args.get('search', '').strip()
        if search_term:
            search_filter = or_(
                Event.title.ilike(f'%{search_term}%'),
                Event.description.ilike(f'%{search_term}%'),
                Event.short_description.ilike(f'%{search_term}%')
            )
            query = query.filter(search_filter)
        
        # Category filter
        category_param = request.args.get('category', '').strip()
        if category_param:
            category_filter = or_(
                Category.name.ilike(f'%{category_param}%'),
                Category.slug.ilike(f'%{category_param}%')
            )
            query = query.join(Event.categories).filter(category_filter)
        
        # Location filter
        location = request.args.get('location', '').strip()
        if location:
            query = query.filter(Event.location.ilike(f'%{location}%'))
        
        # Upcoming events filter
        upcoming = request.args.get('upcoming', '').lower()
        if upcoming == 'true':
            query = query.filter(Event.date > datetime.utcnow())
        
        # Sorting (default: upcoming events first, then by date)
        sort_by = request.args.get('sort', 'date')
        if sort_by == 'price':
            query = query.order_by(Event.price.asc())
        elif sort_by == 'title':
            query = query.order_by(Event.title.asc())
        else:  # default to date
            query = query.order_by(Event.date.asc())
        
        # Pagination
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        limit = min(limit, 100)  # Cap at 100 items per page
        
        # Execute query with pagination
        events_paginated = query.paginate(
            page=page, 
            per_page=limit, 
            error_out=False
        )
        
        events = events_paginated.items
        
        return jsonify({
            'success': True,
            'events': [event.to_summary_dict() for event in events],
            'pagination': {
                'current_page': page,
                'total_pages': events_paginated.pages,
                'total_items': events_paginated.total,
                'items_per_page': limit,
                'has_next': events_paginated.has_next,
                'has_prev': events_paginated.has_prev
            },
            'filters_applied': {
                'search': search_term or None,
                'category': category_param or None,
                'location': location or None,
                'upcoming_only': upcoming == 'true'
            }
        }), 200
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': 'Invalid pagination parameters',
            'details': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch events',
            'details': str(e)
        }), 500

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    #single event by ID with full details
    try:
        event = Event.query.filter_by(id=event_id, is_active=True).first()
        
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found',
                'message': f'No active event found with ID {event_id}'
            }), 404
        
        return jsonify({
            'success': True,
            'event': event.to_dict(include_categories=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch event',
            'details': str(e)
        }), 500

@event_bp.route('/events/slug/<string:event_slug>', methods=['GET'])
def get_event_by_slug(event_slug):
    #Get a single event by slug with full details
    try:
        event = Event.query.filter_by(slug=event_slug, is_active=True).first()
        
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found',
                'message': f'No active event found with slug "{event_slug}"'
            }), 404
        
        return jsonify({
            'success': True,
            'event': event.to_dict(include_categories=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch event',
            'details': str(e)
        }), 500

@event_bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    #Get upcoming events only
    try:
        limit = int(request.args.get('limit', 10))
        limit = min(limit, 50)  # Cap at 50
        
        events = Event.query.filter(
            Event.is_active == True,
            Event.date > datetime.utcnow()
        ).order_by(Event.date.asc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'events': [event.to_summary_dict() for event in events],
            'count': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch upcoming events',
            'details': str(e)
        }), 500