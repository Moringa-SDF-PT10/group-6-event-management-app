from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from app import db
from datetime import datetime

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    
    # Define serialization rules to include relationships
    serialize_rules = ('-organizer.password_hash', '-tickets.user.password_hash', '-categories.events')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    organizer = db.relationship('User', backref=db.backref('events', lazy=True))
    tickets = db.relationship('Ticket', backref='event', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', secondary='event_categories', back_populates='events')

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

    @validates('date')
    def validate_date(self, key, value):
        if isinstance(value, str):
            # If string is passed, try to parse it
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid date format. Use ISO format.")
        
        if value < datetime.now():
            raise ValueError("Event date cannot be in the past")
        return value

    def to_dict(self, include_organizer=True, include_categories=True):
        
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'price': self.price,
            'image_url': self.image_url,
            'organizer_id': self.organizer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_organizer and self.organizer:
            data['organizer'] = {
                'id': self.organizer.id,
                'username': self.organizer.username,
                'first_name': self.organizer.first_name,
                'last_name': self.organizer.last_name
            }
        
        if include_categories:
            data['categories'] = [{'id': cat.id, 'name': cat.name} for cat in self.categories]
            
        return data