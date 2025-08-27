from sqlalchemy import Enum
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from app import db, bcrypt

ROLE_ATTENDEE = "attendee"
ROLE_ORGANIZER = "organizer"
VALID_ROLES = {ROLE_ATTENDEE, ROLE_ORGANIZER}

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password_hash',)

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(Enum(*VALID_ROLES, name="role_enum"), nullable=False, default=ROLE_ATTENDEE)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @validates("role")
    def validate_role(self, key, value):
        if value not in VALID_ROLES:
            raise ValueError(f"Invalid role: '{value}'. Must be one of {VALID_ROLES}")
        return value

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)