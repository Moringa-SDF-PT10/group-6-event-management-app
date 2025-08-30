from app import db
from datetime import datetime, timezone

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='tickets')

    def __repr__(self):
        return f'<{self.quantity} Ticket(s) for Event ID {self.event_id} by User ID {self.user_id}>'

    def to_dict(self, include_event=False):
        data = {
            'id': self.id,
            'purchase_date': self.purchase_date.isoformat(),
            'quantity': self.quantity,
            'user_id': self.user_id,
            'event_id': self.event_id
        }
        if include_event and self.event:
            data['event'] = self.event.to_summary_dict()
        return data