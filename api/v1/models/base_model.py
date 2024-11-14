#!/usr/bin/env python3

# Imports
from datetime import datetime
import uuid
from api.db.database import db


class BaseModel(db.Model):
    """Base model for all other models"""

    # this ensures that this model is not created as a table in the db
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Saves the current instance to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Deletes the current instance from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        """returns a dictionary representation of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        obj_dict["id"] = self.id
        if self.created_at:
            obj_dict["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
