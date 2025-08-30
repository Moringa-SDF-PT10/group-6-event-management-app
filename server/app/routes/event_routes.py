from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models.event import Event
from app.models.category import Category
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

event_bp = Blueprint("events", __name__)

#PUBLIC ROUTES

#Route for Top Picks section
@event_bp.route("/top-picks", methods=["GET"])
def get_top_picks():
    """Fetches the top 4 most expensive upcoming events."""
    events = Event.query.filter(
        Event.is_active == True,
        Event.date > datetime.utcnow()
    ).order_by(Event.price.desc()).limit(4).all()
    return jsonify([event.to_summary_dict() for event in events])

#Route for Featured Events section
@event_bp.route("/featured", methods=["GET"])
def get_featured_events():
    """Fetches the top 8 soonest upcoming events."""
    events = Event.query.filter(
        Event.is_active == True,
        Event.date > datetime.utcnow()
    ).order_by(Event.date.asc()).limit(8).all()
    return jsonify([event.to_summary_dict() for event in events])


@event_bp.route("/", methods=["GET"])
def get_events():
    """Browse/filter/search/paginate events"""
    query = Event.query.filter_by(is_active=True)

    search_term = request.args.get("search", "").strip()
    if search_term:
        query = query.filter(or_(
            Event.title.ilike(f"%{search_term}%"),
            Event.description.ilike(f"%{search_term}%"),
            Event.short_description.ilike(f"%{search_term}%")
        ))

    category_param = request.args.get("category", "").strip()
    if category_param:
        query = query.join(Event.categories).filter(or_(
            Category.name.ilike(f"%{category_param}%"),
            Category.slug.ilike(f"%{category_param}%")
        ))

    location = request.args.get("location", "").strip()
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))

    upcoming = request.args.get("upcoming", "").lower()
    if upcoming == "true":
        query = query.filter(Event.date > datetime.utcnow())

    sort_by = request.args.get("sort", "date")
    if sort_by == "price":
        query = query.order_by(Event.price.asc())
    elif sort_by == "title":
        query = query.order_by(Event.title.asc())
    else:
        query = query.order_by(Event.date.asc())

    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 20)), 100)
    events_paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "success": True,
        "events": [event.to_summary_dict() for event in events_paginated.items],
        "pagination": {
            "current_page": page,
            "total_pages": events_paginated.pages,
            "total_items": events_paginated.total,
            "items_per_page": limit,
            "has_next": events_paginated.has_next,
            "has_prev": events_paginated.has_prev,
        }
    })

@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    event = Event.query.filter_by(id=event_id, is_active=True).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict(include_categories=True))

@event_bp.route("/slug/<string:event_slug>", methods=["GET"])
def get_event_by_slug(event_slug):
    event = Event.query.filter_by(slug=event_slug, is_active=True).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict(include_categories=True))

@event_bp.route("/upcoming", methods=["GET"])
def get_upcoming_events():
    limit = min(int(request.args.get("limit", 10)), 50)
    events = Event.query.filter(
        Event.is_active == True,
        Event.date > datetime.utcnow()
    ).order_by(Event.date.asc()).limit(limit).all()
    return jsonify([event.to_summary_dict() for event in events])

#ORGANIZER CRUD ROUTES

@event_bp.route("/", methods=["POST"])
@role_required(["organizer"])
def create_event():
    try:
        data = request.form.to_dict()
        organizer_id = get_jwt_identity()

        required_fields = ['title', 'description', 'date', 'price', 'max_attendees', 'location', 'venue']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        image_url_path = None
        if "image_url" in request.files:
            file = request.files["image_url"]
            if file and file.filename:
                upload_folder = current_app.config.get("UPLOAD_FOLDER")
                if upload_folder:
                    os.makedirs(upload_folder, exist_ok=True)
                    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    image_url_path = f"/uploads/{filename}"

        new_event = Event(
            title=data.get("title"),
            description=data.get("description"),
            short_description=data.get("description", "")[:150],
            date=datetime.fromisoformat(data.get("date").replace("Z", "+00:00")),
            price=float(data.get("price")),
            max_attendees=int(data.get("max_attendees")),
            location=data.get("location"),
            venue=data.get("venue"),
            image_url=image_url_path,
            organizer_id=organizer_id,
            slug=Event.create_slug(data.get("title"))
        )
        
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            "message": "Event created successfully",
            "event": new_event.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating event: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

@event_bp.route("/<int:id>", methods=["PATCH"])
@role_required(["organizer"])
def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    organizer_id_from_token = get_jwt_identity()
    if str(event.organizer_id) != str(organizer_id_from_token):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.form.to_dict() if request.files else request.get_json()

    if "image_url" in request.files:
        file = request.files["image_url"]
        if file and file.filename:
            upload_folder = current_app.config.get("UPLOAD_FOLDER")
            if upload_folder:
                os.makedirs(upload_folder, exist_ok=True)
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                event.image_url = f"/uploads/{filename}"

    for key, value in data.items():
        if hasattr(event, key) and key not in ["image_url", "id", "slug", "organizer_id"]:
            if key == 'date' and value:
                event.date = datetime.fromisoformat(value.replace("Z", "+00:00"))
            else:
                 setattr(event, key, value)

    db.session.commit()
    return jsonify({"message": "Event updated", "event": event.to_dict()})

@event_bp.route("/<int:id>", methods=["DELETE"])
@role_required(["organizer"])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    organizer_id_from_token = get_jwt_identity()
    if str(event.organizer_id) != str(organizer_id_from_token):
        return jsonify({"error": "Unauthorized"}), 403
        
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})

