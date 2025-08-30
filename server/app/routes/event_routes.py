from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models.event import Event
from app.models.category import Category
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_
from datetime import datetime
import os, uuid
from werkzeug.utils import secure_filename

event_bp = Blueprint("events", __name__, url_prefix="/events")

# ---------- PUBLIC ROUTES ----------

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

# ---------- ORGANIZER CRUD ROUTES ----------

@event_bp.route("/", methods=["POST"])
@role_required(["organizer"])
def create_event():
    banner_image_url = None
    if "banner_image" in request.files:
        file = request.files["banner_image"]
        if file:
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            banner_image_url = f"/uploads/{filename}"
        data = request.form.to_dict()
    else:
        data = request.get_json()
        banner_image_url = data.get("banner_image_url")

    organizer_id = get_jwt_identity()
    new_event = Event.create({
        "name": data.get("name"),
        "description": data.get("description"),
        "date": data.get("date"),
        "price": data.get("price"),
        "capacity": data.get("capacity"),
        "banner_image_url": banner_image_url
    }, organizer_id)

    return jsonify({
        "message": "Event created successfully",
        "event": new_event.to_dict()
    }), 201

@event_bp.route("/<int:id>", methods=["PATCH"])
@role_required(["organizer"])
def update_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if event.organizer_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403

    if "banner_image" in request.files:
        file = request.files["banner_image"]
        if file:
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            event.banner_image_url = f"/uploads/{filename}"
        data = request.form.to_dict()
    else:
        data = request.get_json()
        if "banner_image_url" in data:
            event.banner_image_url = data["banner_image_url"]

    for key, value in data.items():
        if hasattr(event, key) and key != "banner_image_url":
            setattr(event, key, value)

    db.session.commit()
    return jsonify({"message": "Event updated", "event": event.to_dict()})

@event_bp.route("/<int:id>", methods=["DELETE"])
@role_required(["organizer"])
def delete_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if event.organizer_id != get_jwt_identity():
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})
