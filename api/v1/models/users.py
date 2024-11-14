#!/usr/bin/env python3

# imports
import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from api.db.database import db
from api.v1.models.base_model import BaseModel


class User(BaseModel):
    """A class that defines users info"""

    __tablename__ = "users"

    first_name = db.Column(db.String(36), nullable=False)
    last_name = db.Column(db.String(36), nullable=False)
    username = db.Column(db.String(36), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    avatar_url = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_superadmin = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.username}>"

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
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        return obj_dict

    def set_password(self, password):
        """Hashes a plain-text password and stores it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password hash against a plain-text password."""
        return check_password_hash(self.password, password)

    # validation check for email format
    def validate_email(self, email):
        """a regex expression for a simple email format check"""
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
