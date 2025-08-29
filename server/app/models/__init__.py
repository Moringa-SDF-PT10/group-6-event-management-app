from .user import User
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

db = SQLAlchemy()

# Models for Event Management and Tracking System
event_categories = db.Table(
    'event_categories',
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='attendee')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    events = db.relationship('Event', backref='organizer', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "events": [event.id for event in self.events],
            "tickets": [ticket.id for ticket in self.tickets]
        }

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    categories = db.relationship('Category', secondary=event_categories, backref='events')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat(),
            "location": self.location,
            "price": self.price,
            "image_url": self.image_url,
            "organizer_id": self.organizer_id,
            "created_at": self.created_at.isoformat(),
            "categories": [category.name for category in self.categories],
            "tickets": [ticket.id for ticket in self.tickets]
        }

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(20), nullable=False, default='Regular')
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_type": self.ticket_type,
            "purchase_date": self.purchase_date.isoformat(),
            "user_id": self.user_id,
            "event_id": self.event_id
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }