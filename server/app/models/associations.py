from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many-to-many association table for events and categories
event_categories = db.Table('event_categories',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)