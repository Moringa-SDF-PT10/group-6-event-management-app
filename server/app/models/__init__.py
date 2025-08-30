from app import db

# Import all models so they are registered with SQLAlchemy
from app.models.category import Category
from app.models.event import Event
from app.models.associations import event_categories
from app.models.user import User

__all__ = ['db', 'Category', 'Event', 'event_categories', 'User', 'Ticket']
