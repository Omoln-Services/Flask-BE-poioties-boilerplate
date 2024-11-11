#!/usr/bin/env python3

# imports
from app import db
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """A class that defines users info
    """
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    first_name = db.Column(db.String(36), nullable=False)
    last_name = db.Column(db.String(36), nullable=False)
    username = db.Column(db.String(36), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, server_default="true")
    is_superadmin = db.Column(db.Boolean, server_default="false")
    is_deleted = db.Column(db.Boolean, server_default="false")
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
    
    def to_dict(self):
        """Convert the user object to a dictionary format, excluding sensitive fields."""
        obj_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_superadmin": self.is_superadmin,
            "is_deleted": self.is_deleted,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
        return obj_dict

    def set_password(self, password):
        """Hashes a plain-text password and stores it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password hash against a plain-text password."""
        return check_password_hash(self.password, password)
