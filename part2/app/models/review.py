"""Review model for HBnB application."""
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review entity with validation and relationships."""

    def __init__(self, text, rating, place, user):
        """Initialize review with required attributes."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Get text."""
        return self.__text

    @text.setter
    def text(self, value):
        """Set text with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Text is required")
        self.__text = value

    @property
    def rating(self):
        """Get rating."""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Set rating with validation."""
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        self.__rating = value