from .user import User
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

# Models for Event Management and Tracking System
    
class User(db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
        tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    
        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "tickets": [ticket.to_dict(include_user=False) for ticket in self.tickets]
            }
    
class Category(db.Model):
        __tablename__ = "categories"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        events = relationship("Event", back_populates="category", cascade="all, delete-orphan")
    
        def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "events": [event.to_dict(include_category=False) for event in self.events]
            }
    
class Event(db.Model):
        __tablename__ = "events"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        description = db.Column(db.String, nullable=False)
        date = db.Column(db.DateTime, nullable=False)
        location = db.Column(db.String, nullable=False)
        category_id = db.Column(db.Integer, ForeignKey("categories.id"), nullable=False)
        category = relationship("Category", back_populates="events")
        tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")
    
        def to_dict(self, include_category=True):
            data = {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "date": self.date.isoformat(),
                "location": self.location,
                "category_id": self.category_id,
                "tickets": [ticket.to_dict(include_event=False) for ticket in self.tickets]
            }
            if include_category:
                data["category"] = self.category.to_dict() if self.category else None
            return data
    
class Ticket(db.Model):
        __tablename__ = "tickets"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
        event_id = db.Column(db.Integer, ForeignKey("events.id"), nullable=False)
        purchase_date = db.Column(db.DateTime, nullable=False)
        user = relationship("User", back_populates="tickets")
        event = relationship("Event", back_populates="tickets")
    
        def to_dict(self, include_user=True, include_event=True):
            data = {
                "id": self.id,
                "user_id": self.user_id,
                "event_id": self.event_id,
                "purchase_date": self.purchase_date.isoformat()
            }
            if include_user:
                data["user"] = self.user.to_dict() if self.user else None
            if include_event:
                data["event"] = self.event.to_dict(include_category=False) if self.event else None
            return data
