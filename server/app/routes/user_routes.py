from flask import Blueprint, jsonify
from app.auth_decorators import role_required
from flask_jwt_extended import get_jwt, get_jwt_identity
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket
from app import db
from sqlalchemy import func, distinct
from datetime import datetime, date, timedelta

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/organizer/events', methods=['GET'])
@role_required(['organizer'])
def get_organizer_events():
    """Fetches all events created by the logged-in organizer."""
    organizer_id = get_jwt_identity()
    events = Event.query.filter_by(organizer_id=organizer_id).order_by(Event.date.desc()).all()
    return jsonify([event.to_dict(include_categories=False) for event in events])

@user_bp.route('/attendee/tickets', methods=['GET'])
@role_required(['attendee'])
def get_attendee_tickets():
    """Fetches all tickets for the logged-in attendee."""
    user_id = get_jwt_identity()
    tickets = Ticket.query.filter_by(user_id=user_id).join(Event).order_by(Event.date.asc()).all()
    return jsonify([ticket.to_dict(include_event=True) for ticket in tickets])

@user_bp.route('/attendee/tickets/<int:ticket_id>', methods=['GET'])
@role_required(['attendee'])
def get_ticket_details(ticket_id):
    """Fetches details for a single ticket, ensuring it belongs to the user."""
    user_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id=ticket_id, user_id=user_id).first()
    
    if not ticket:
        return jsonify({"error": "Ticket not found or you do not have permission to view it."}), 404
        
    return jsonify(ticket.to_dict(include_event=True))

@user_bp.route('/organizer/stats', methods=['GET'])
@role_required(['organizer'])
def get_organizer_stats():
    """Calculates and returns key statistics for the organizer."""
    organizer_id = get_jwt_identity()

    # Total revenue from all tickets sold
    total_revenue_query = db.session.query(func.sum(Event.price * Ticket.quantity))\
        .join(Ticket, Ticket.event_id == Event.id)\
        .filter(Event.organizer_id == organizer_id).scalar()
    
    # Total tickets sold this month
    today = date.today()
    start_of_month = today.replace(day=1)
    tickets_this_month_query = db.session.query(func.sum(Ticket.quantity))\
        .join(Event, Ticket.event_id == Event.id)\
        .filter(Event.organizer_id == organizer_id, Ticket.purchase_date >= start_of_month).scalar()

    #Calculates unique new attendees in the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_attendees_query = db.session.query(func.count(distinct(Ticket.user_id)))\
        .join(Event, Ticket.event_id == Event.id)\
        .filter(Event.organizer_id == organizer_id, Ticket.purchase_date >= thirty_days_ago).scalar()

    stats = {
        "total_revenue": total_revenue_query or 0,
        "tickets_this_month": tickets_this_month_query or 0,
        "new_attendees": new_attendees_query or 0
    }
    
    return jsonify(stats)

@user_bp.route('/dashboard', methods=['GET'])
@role_required(['organizer', 'attendee'])
def dashboard():
    claims = get_jwt()
    user_role = claims.get('role')
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user_role == 'organizer':
        events_created_count = Event.query.filter_by(organizer_id=user_id).count()
        return jsonify(
            message=f"Welcome to your Organizer Dashboard, {user.username}!",
            role=user_role,
            events_created=events_created_count,
        ), 200
    
    elif user_role == 'attendee':
        ticket_count = Ticket.query.filter_by(user_id=user_id).count()
        return jsonify(
            message=f"Welcome to your Attendee Dashboard, {user.username}!",
            role=user_role,
            tickets_purchased=ticket_count,
        ), 200