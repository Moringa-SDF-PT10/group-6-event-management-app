from datetime import datetime
from app.models import db

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String, nullable=False, default="Regular")
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="tickets")
    event = db.relationship("Event", back_populates="tickets")

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_type": self.ticket_type,
            "purchase_date": self.purchase_date.isoformat(),
            "user_id": self.user_id,
            "event_id": self.event_id,
        }
