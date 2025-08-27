from app import db
from app.models.associations import event_categories
from datetime import datetime,timezone

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    venue = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(3), nullable=False, default='KSH')
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    max_attendees = db.Column(db.Integer, nullable=True)
    slug = db.Column(db.String(250), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
     
    # Many-to-many relationship with Category
    categories = db.relationship('Category', 
                               secondary=event_categories,
                               lazy='subquery',
                               backref=db.backref('events', lazy=True))
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    def to_dict(self, include_categories=True):
        
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.short_description,
            'date': self.date.isoformat() if self.date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'venue': self.venue,
            'price': self.price,
            'currency': self.currency,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'max_attendees': self.max_attendees,
            'slug': self.slug,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_categories:
            data['categories'] = [category.to_dict() for category in self.categories]
            
        return data
    def to_summary_dict(self):
        
        return {
            'id': self.id,
            'title': self.title,
            'short_description': self.short_description,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'price': self.price,
            'currency': self.currency,
            'image_url': self.image_url,
            'slug': self.slug,
            'categories': [{'id': cat.id, 'name': cat.name, 'slug': cat.slug} for cat in self.categories]
        }
    
    @property
    def is_upcoming(self):
        #check when the event will be in terms of when 
        return self.date > datetime.now(timezone.utc) if self.date else False
    
    @property
    def formatted_price(self):
        # simply this function is returning a formatted price string
        if self.price == 0:
            return "Free"
        return f"{self.currency} {self.price:,.0f}"
    
    @staticmethod
    def create_slug(title):
        import re
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug[:250]  # Limit length

