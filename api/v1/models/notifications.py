#!/usr/bin/env python3

# Import
from api.v1.models.base_model import BaseModel
from api.db.database import db


class Notifications(BaseModel):
    """Defines the Notifications model requirement"""

    title = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False)
