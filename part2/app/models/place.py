"""Place model for HBnB application."""
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place entity with validation and relationships."""

    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        """Initialize place with required attributes."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """Get title."""
        return self.__title

    @title.setter
    def title(self, value):
        """Set title with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Title is required")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters or less")
        self.__title = value

    @property
    def price(self):
        """Get price."""
        return self.__price

    @price.setter
    def price(self, value):
        """Set price with validation."""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self.__price = float(value)

    @property
    def latitude(self):
        """Get latitude."""
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Set latitude with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self.__latitude = float(value)

    @property
    def longitude(self):
        """Get longitude."""
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Set longitude with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self.__longitude = float(value)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)