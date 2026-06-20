"""Amenity model for HBnB application."""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity with validation."""

    def __init__(self, name):
        """Initialize amenity with required attributes."""
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Get name."""
        return self.__name

    @name.setter
    def name(self, value):
        """Set name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Name is required")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or less")
        self.__name = value