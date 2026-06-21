"""Tests for HBnB Evolution Part 2 API endpoints."""
import pytest
from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


# ─────────────────────────────────────────────
# USER TESTS
# ─────────────────────────────────────────────

class TestUsers:
    """Tests for /api/v1/users/ endpoints."""

    def test_create_user_success(self, client):
        """POST /users/ — valid data returns 201."""
        response = client.post('/api/v1/users/', json={
            'first_name': 'Jorge',
            'last_name': 'Burgos',
            'email': 'jorge@test.com'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'jorge@test.com'
        assert 'id' in data

    def test_create_user_duplicate_email(self, client):
        """POST /users/ — duplicate email returns 400."""
        payload = {
            'first_name': 'Ana',
            'last_name': 'Lopez',
            'email': 'duplicate@test.com'
        }
        client.post('/api/v1/users/', json=payload)
        response = client.post('/api/v1/users/', json=payload)
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_create_user_missing_field(self, client):
        """POST /users/ — missing required field returns 400."""
        response = client.post('/api/v1/users/', json={
            'first_name': 'Solo'
        })
        assert response.status_code == 400

    def test_get_all_users(self, client):
        """GET /users/ — returns list."""
        client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'list@test.com'
        })
        response = client.get('/api/v1/users/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_get_user_by_id(self, client):
        """GET /users/<id> — returns user details."""
        create = client.post('/api/v1/users/', json={
            'first_name': 'Maria',
            'last_name': 'Torres',
            'email': 'maria@test.com'
        })
        user_id = create.get_json()['id']
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200
        assert response.get_json()['id'] == user_id

    def test_get_user_not_found(self, client):
        """GET /users/<bad_id> — returns 404."""
        response = client.get('/api/v1/users/nonexistent-id')
        assert response.status_code == 404

    def test_update_user(self, client):
        """PUT /users/<id> — updates user successfully."""
        create = client.post('/api/v1/users/', json={
            'first_name': 'Before',
            'last_name': 'Update',
            'email': 'update@test.com'
        })
        user_id = create.get_json()['id']
        response = client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'After',
            'last_name': 'Update',
            'email': 'update@test.com'
        })
        assert response.status_code == 200
        assert response.get_json()['first_name'] == 'After'

    def test_update_user_not_found(self, client):
        """PUT /users/<bad_id> — returns 404."""
        response = client.put('/api/v1/users/nonexistent-id', json={
            'first_name': 'X',
            'last_name': 'Y',
            'email': 'x@test.com'
        })
        assert response.status_code == 404


# ─────────────────────────────────────────────
# AMENITY TESTS
# ─────────────────────────────────────────────

class TestAmenities:
    """Tests for /api/v1/amenities/ endpoints."""

    def test_create_amenity_success(self, client):
        """POST /amenities/ — valid data returns 201."""
        response = client.post('/api/v1/amenities/', json={'name': 'WiFi'})
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'WiFi'
        assert 'id' in data

    def test_create_amenity_missing_name(self, client):
        """POST /amenities/ — missing name returns 400."""
        response = client.post('/api/v1/amenities/', json={})
        assert response.status_code == 400

    def test_get_all_amenities(self, client):
        """GET /amenities/ — returns list."""
        client.post('/api/v1/amenities/', json={'name': 'Pool'})
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_get_amenity_by_id(self, client):
        """GET /amenities/<id> — returns amenity."""
        create = client.post('/api/v1/amenities/', json={'name': 'Parking'})
        amenity_id = create.get_json()['id']
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        assert response.status_code == 200
        assert response.get_json()['id'] == amenity_id

    def test_get_amenity_not_found(self, client):
        """GET /amenities/<bad_id> — returns 404."""
        response = client.get('/api/v1/amenities/nonexistent-id')
        assert response.status_code == 404

    def test_update_amenity(self, client):
        """PUT /amenities/<id> — updates amenity."""
        create = client.post('/api/v1/amenities/', json={'name': 'OldName'})
        amenity_id = create.get_json()['id']
        response = client.put(f'/api/v1/amenities/{amenity_id}',
                              json={'name': 'NewName'})
        assert response.status_code == 200
        assert response.get_json()['name'] == 'NewName'

    def test_update_amenity_not_found(self, client):
        """PUT /amenities/<bad_id> — returns 404."""
        response = client.put('/api/v1/amenities/nonexistent-id',
                              json={'name': 'X'})
        assert response.status_code == 404


# ─────────────────────────────────────────────
# PLACE TESTS
# ─────────────────────────────────────────────

class TestPlaces:
    """Tests for /api/v1/places/ endpoints."""

    def _create_owner(self, client, email='owner@test.com'):
        """Helper: create a user to use as place owner."""
        r = client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'User',
            'email': email
        })
        return r.get_json()['id']

    def test_create_place_success(self, client):
        """POST /places/ — valid data returns 201."""
        owner_id = self._create_owner(client, 'place_owner@test.com')
        response = client.post('/api/v1/places/', json={
            'title': 'Casa Bonita',
            'description': 'Frente al mar',
            'price': 120.0,
            'latitude': 18.4655,
            'longitude': -66.1057,
            'owner_id': owner_id,
            'amenities': []
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Casa Bonita'
        assert 'id' in data

    def test_create_place_invalid_owner(self, client):
        """POST /places/ — bad owner_id returns 400."""
        response = client.post('/api/v1/places/', json={
            'title': 'Fantasma',
            'description': 'No owner',
            'price': 50.0,
            'latitude': 18.0,
            'longitude': -66.0,
            'owner_id': 'nonexistent-owner',
            'amenities': []
        })
        assert response.status_code == 400

    def test_create_place_missing_fields(self, client):
        """POST /places/ — missing required fields returns 400."""
        response = client.post('/api/v1/places/', json={'title': 'Solo titulo'})
        assert response.status_code == 400

    def test_get_all_places(self, client):
        """GET /places/ — returns list."""
        owner_id = self._create_owner(client, 'list_owner@test.com')
        client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Desc',
            'price': 75.0,
            'latitude': 18.0,
            'longitude': -66.0,
            'owner_id': owner_id,
            'amenities': []
        })
        response = client.get('/api/v1/places/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_get_place_by_id(self, client):
        """GET /places/<id> — returns place details."""
        owner_id = self._create_owner(client, 'getplace@test.com')
        create = client.post('/api/v1/places/', json={
            'title': 'Mi Casa',
            'description': 'Linda',
            'price': 90.0,
            'latitude': 18.1,
            'longitude': -66.1,
            'owner_id': owner_id,
            'amenities': []
        })
        place_id = create.get_json()['id']
        response = client.get(f'/api/v1/places/{place_id}')
        assert response.status_code == 200
        assert response.get_json()['id'] == place_id

    def test_get_place_not_found(self, client):
        """GET /places/<bad_id> — returns 404."""
        response = client.get('/api/v1/places/nonexistent-id')
        assert response.status_code == 404

    def test_update_place(self, client):
        """PUT /places/<id> — updates place."""
        owner_id = self._create_owner(client, 'update_place@test.com')
        create = client.post('/api/v1/places/', json={
            'title': 'Original',
            'description': 'Antes',
            'price': 100.0,
            'latitude': 18.2,
            'longitude': -66.2,
            'owner_id': owner_id,
            'amenities': []
        })
        place_id = create.get_json()['id']
        response = client.put(f'/api/v1/places/{place_id}', json={
            'title': 'Actualizado',
            'description': 'Despues',
            'price': 150.0,
            'latitude': 18.2,
            'longitude': -66.2,
            'owner_id': owner_id,
            'amenities': []
        })
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Actualizado'

    def test_update_place_not_found(self, client):
        """PUT /places/<bad_id> — returns 404."""
        response = client.put('/api/v1/places/nonexistent-id', json={
            'title': 'X', 'price': 10.0,
            'latitude': 0.0, 'longitude': 0.0,
            'owner_id': 'x', 'amenities': []
        })
        assert response.status_code == 404


# ─────────────────────────────────────────────
# REVIEW TESTS
# ─────────────────────────────────────────────

class TestReviews:
    """Tests for /api/v1/reviews/ endpoints."""

    def _setup(self, client, suffix=''):
        """Helper: create user and place for review tests."""
        user = client.post('/api/v1/users/', json={
            'first_name': 'Reviewer',
            'last_name': 'Test',
            'email': f'reviewer{suffix}@test.com'
        }).get_json()
        place = client.post('/api/v1/places/', json={
            'title': f'Review Place {suffix}',
            'description': 'Para reviews',
            'price': 80.0,
            'latitude': 18.3,
            'longitude': -66.3,
            'owner_id': user['id'],
            'amenities': []
        }).get_json()
        return user['id'], place['id']

    def test_create_review_success(self, client):
        """POST /reviews/ — valid data returns 201."""
        user_id, place_id = self._setup(client, '1')
        response = client.post('/api/v1/reviews/', json={
            'text': 'Excelente lugar!',
            'rating': 5,
            'user_id': user_id,
            'place_id': place_id
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['rating'] == 5
        assert 'id' in data

    def test_create_review_invalid_user(self, client):
        """POST /reviews/ — bad user_id returns 400."""
        _, place_id = self._setup(client, '2')
        response = client.post('/api/v1/reviews/', json={
            'text': 'Bad user',
            'rating': 3,
            'user_id': 'nonexistent-user',
            'place_id': place_id
        })
        assert response.status_code == 400

    def test_create_review_invalid_place(self, client):
        """POST /reviews/ — bad place_id returns 400."""
        user_id, _ = self._setup(client, '3')
        response = client.post('/api/v1/reviews/', json={
            'text': 'Bad place',
            'rating': 3,
            'user_id': user_id,
            'place_id': 'nonexistent-place'
        })
        assert response.status_code == 400

    def test_create_review_invalid_rating(self, client):
        """POST /reviews/ — rating out of range returns 400."""
        user_id, place_id = self._setup(client, '4')
        response = client.post('/api/v1/reviews/', json={
            'text': 'Bad rating',
            'rating': 10,
            'user_id': user_id,
            'place_id': place_id
        })
        assert response.status_code == 400

    def test_get_all_reviews(self, client):
        """GET /reviews/ — returns list."""
        user_id, place_id = self._setup(client, '5')
        client.post('/api/v1/reviews/', json={
            'text': 'Bueno',
            'rating': 4,
            'user_id': user_id,
            'place_id': place_id
        })
        response = client.get('/api/v1/reviews/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_get_review_by_id(self, client):
        """GET /reviews/<id> — returns review."""
        user_id, place_id = self._setup(client, '6')
        create = client.post('/api/v1/reviews/', json={
            'text': 'Muy bien',
            'rating': 4,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create.get_json()['id']
        response = client.get(f'/api/v1/reviews/{review_id}')
        assert response.status_code == 200
        assert response.get_json()['id'] == review_id

    def test_get_review_not_found(self, client):
        """GET /reviews/<bad_id> — returns 404."""
        response = client.get('/api/v1/reviews/nonexistent-id')
        assert response.status_code == 404

    def test_update_review(self, client):
        """PUT /reviews/<id> — updates review."""
        user_id, place_id = self._setup(client, '7')
        create = client.post('/api/v1/reviews/', json={
            'text': 'Antes',
            'rating': 3,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create.get_json()['id']
        response = client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Despues',
            'rating': 5,
            'user_id': user_id,
            'place_id': place_id
        })
        assert response.status_code == 200
        assert response.get_json()['rating'] == 5

    def test_update_review_not_found(self, client):
        """PUT /reviews/<bad_id> — returns 404."""
        response = client.put('/api/v1/reviews/nonexistent-id', json={
            'text': 'X', 'rating': 1,
            'user_id': 'x', 'place_id': 'x'
        })
        assert response.status_code == 404

    def test_delete_review(self, client):
        """DELETE /reviews/<id> — returns 200."""
        user_id, place_id = self._setup(client, '8')
        create = client.post('/api/v1/reviews/', json={
            'text': 'Para borrar',
            'rating': 2,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create.get_json()['id']
        response = client.delete(f'/api/v1/reviews/{review_id}')
        assert response.status_code == 200
        # Verify it's gone
        get = client.get(f'/api/v1/reviews/{review_id}')
        assert get.status_code == 404

    def test_delete_review_not_found(self, client):
        """DELETE /reviews/<bad_id> — returns 404."""
        response = client.delete('/api/v1/reviews/nonexistent-id')
        assert response.status_code == 404

    def test_get_reviews_by_place(self, client):
        """GET /reviews/places/<place_id>/reviews — returns reviews for place."""
        user_id, place_id = self._setup(client, '9')
        client.post('/api/v1/reviews/', json={
            'text': 'Para este place',
            'rating': 5,
            'user_id': user_id,
            'place_id': place_id
        })
        response = client.get(f'/api/v1/reviews/places/{place_id}/reviews')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert any(r['place_id'] == place_id for r in data)

    def test_get_reviews_by_place_not_found(self, client):
        """GET /reviews/places/<bad_id>/reviews — returns 404."""
        response = client.get('/api/v1/reviews/places/nonexistent-id/reviews')
        assert response.status_code == 404
