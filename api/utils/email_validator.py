#!/usr/bin/env python3

# Import
import re


# validation check for email format
def validate_email(email):
    """Check if an email is in a valid format."""
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, email))