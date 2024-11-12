#!/usr/bin/env python3


# Import
from api.v1.models.base_model import BaseModel
from app import db


class EmailTemplate(BaseModel):
    """This model defines the email template requirement
    """
    title = db.Column(db.Text, nullable=False)
    template = db.Column(db.Text, nullable=False)
    type = db.Column(db.String, nullable=False)
    template_status = db.Column(db.Enum(
        "online", "offline", name="template_status"),
        default='online',
        nullable=False
    )