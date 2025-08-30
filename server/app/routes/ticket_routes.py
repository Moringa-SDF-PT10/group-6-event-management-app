from flask import Blueprint, jsonify, request
from app import db
from app.models.ticket import Ticket
from app.models.event import Event
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func

ticket_bp = Blueprint("ticket_bp", __name__)

@ticket_bp.route("/", methods=["POST"])
@role_required(["attendee"])
def purchase_ticket():
    data = request.get_json()
    user_id = get_jwt_identity()
    event_id = data.get('event_id')
    # Get quantity from request, default to 1 
    quantity = data.get('quantity', 1)

    if not event_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Event ID and a valid quantity are required"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    existing_ticket = Ticket.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_ticket:
        return jsonify({"error": "You already have tickets for this event"}), 409

    # -Capacity check
    if event.max_attendees is not None:
        # Sum the quantity of all tickets sold for this event
        tickets_sold = db.session.query(func.sum(Ticket.quantity)).filter(Ticket.event_id == event_id).scalar() or 0
        
        if (tickets_sold + quantity) > event.max_attendees:
            remaining_tickets = event.max_attendees - tickets_sold
            return jsonify({"error": f"Cannot purchase {quantity} tickets. Only {remaining_tickets} tickets remaining."}), 409

    try:
        #  Save ticket with the specified quantity
        new_ticket = Ticket(user_id=user_id, event_id=event_id, quantity=quantity)
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({
            "message": "Ticket purchased successfully!",
            "ticket": new_ticket.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error purchasing ticket: {e}")
        return jsonify({"error": "An error occurred while purchasing the ticket."}), 500