"""Facade pattern for HBnB application."""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade class to manage all layers."""

    def __init__(self):
        """Initialize repositories."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user by ID."""
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
    # Review methods
    def create_review(self, review_data):
        """Create a new review."""
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")
        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """Get review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update review by ID."""
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete review by ID."""
        self.review_repo.delete(review_id)

    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity by ID."""
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # Place methods
    def create_place(self, place_data):
        """Create a new place."""
        owner = self.user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        for amenity in amenities:
            place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place by ID."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner
            del place_data['owner_id']
        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                amenities.append(amenity)
            place.amenities = amenities
            del place_data['amenities']
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)
    