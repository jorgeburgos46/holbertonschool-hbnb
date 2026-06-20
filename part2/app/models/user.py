"""User model for HBnB application."""
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """User entity with validation."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize user with required attributes."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Get first name."""
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """Set first name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("First name is required")
        if len(value) > 50:
            raise ValueError("First name must be 50 characters or less")
        self.__first_name = value

    @property
    def last_name(self):
        """Get last name."""
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """Set last name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Last name is required")
        if len(value) > 50:
            raise ValueError("Last name must be 50 characters or less")
        self.__last_name = value

    @property
    def email(self):
        """Get email."""
        return self.__email

    @email.setter
    def email(self, value):
        """Set email with format validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Email is required")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        self.__email = value