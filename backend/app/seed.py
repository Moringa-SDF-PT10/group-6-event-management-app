from app.models import db, User, Event, Category, Ticket
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_data():
    print("🌱 Seeding database...")

    # --- Clear old data ---
    db.drop_all()
    db.create_all()

    # --- Users (attendee + organizer) ---
    attendee1 = User(
        username="john_doe",
        email="john@example.com",
        _password_hash=generate_password_hash("password123"),
        role="attendee"
    )
    attendee2 = User(
        username="jane_doe",
        email="jane@example.com",
        _password_hash=generate_password_hash("password123"),
        role="attendee"
    )
    organizer1 = User(
        username="event_master",
        email="organizer@example.com",
        _password_hash=generate_password_hash("password123"),
        role="organizer"
    )

    db.session.add_all([attendee1, attendee2, organizer1])
    db.session.commit()

    # --- Categories ---
    music = Category(name="Music")
    tech = Category(name="Tech")
    db.session.add_all([music, tech])
    db.session.commit()

    # --- Events ---
    event1 = Event(
        title="Music Festival 2025",
        description="A grand music festival with live performances.",
        date=datetime.utcnow() + timedelta(days=30),
        location="Nairobi",
        price=20.0,
        image_url="https://via.placeholder.com/300x200",
        organizer_id=organizer1.id,
    )
    event2 = Event(
        title="Tech Summit 2025",
        description="Conference on the latest in technology and startups.",
        date=datetime.utcnow() + timedelta(days=60),
        location="Mombasa",
        price=50.0,
        image_url="https://via.placeholder.com/300x200",
        organizer_id=organizer1.id,
    )

    db.session.add_all([event1, event2])
    db.session.commit()

    # --- Tickets ---
    ticket1 = Ticket(
        ticket_type="Regular",
        user_id=attendee1.id,
        event_id=event1.id,
    )
    ticket2 = Ticke
