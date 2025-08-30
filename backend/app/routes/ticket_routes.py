from flask import Blueprint, request, jsonify
from app.models import db, Ticket, Event
from flask_jwt_extended import jwt_required, get_jwt_identity

ticket_bp = Blueprint("ticket_bp", __name__)

# Buy a ticket
@ticket_bp.route("/tickets", methods=["POST"])
@jwt_required()
def create_ticket():
    data = request.get_json()
    user_id = get_jwt_identity()  # current logged-in user

    event_id = data.get("event_id")
    ticket_type = data.get("ticket_type", "Regular")

    # Validate event
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Create ticket
    ticket = Ticket(user_id=user_id, event_id=event_id, ticket_type=ticket_type)
    db.session.add(ticket)
    db.session.commit()

    return jsonify(ticket.to_dict()), 201
