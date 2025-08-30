from app import db
from datetime import datetime, timezone
from .associations import event_categories

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    events = db.relationship('Event', secondary='event_categories', back_populates='categories')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self, include_events=True):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_events:
            data['events'] = [event.id for event in self.events]
        return data
    
    @staticmethod
    def create_slug(name):
        return name.lower().replace(' ', '-').replace('&', 'and')