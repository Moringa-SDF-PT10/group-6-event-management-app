from datetime import datetime
from .associations import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', secondary='event_categories', back_populates='events')
    organizer = db.relationship('User', backref='events')
    tickets = db.relationship('Ticket', backref='event', cascade='all, delete-orphan')
    
    def to_dict(self, include_categories=True):
        event_dict = {
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
        
        if include_categories:
            event_dict['categories'] = [category.to_dict() for category in self.categories]
            
        return event_dict
    
    @classmethod
    def search_by_title(cls, search_term):
        #Search events by title (case insensitive)
        return cls.query.filter(cls.title.ilike(f'%{search_term}%'))
    
    @classmethod
    def filter_by_category(cls, category_name):
       #Filter events by category name
        return cls.query.join(cls.categories).filter(Category.name.ilike(f'%{category_name}%'))
    
    def __repr__(self):
        return f'<Event {self.title}>'