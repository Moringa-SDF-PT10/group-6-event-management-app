from sqlalchemy_serializer import SerializerMixin
from app import db

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    
    serialize_rules = ('-events.categories',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationships
    events = db.relationship('Event', secondary='event_categories', back_populates='categories')

    def __repr__(self):
        return f'<Category {self.name}>'