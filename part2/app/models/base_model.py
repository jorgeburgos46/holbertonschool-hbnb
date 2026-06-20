"""Base model with common attributes for all entities."""
import uuid
from datetime import datetime


class BaseModel:
    """Base class with id, created_at, and updated_at."""

    def __init__(self):
        """Initialize base attributes."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()