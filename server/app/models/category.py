from .associations import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Back reference to events through association table
    events = db.relationship('Event', secondary='event_categories', back_populates='categories')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'