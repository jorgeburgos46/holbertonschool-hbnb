"""Review endpoints for HBnB API."""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})


def review_to_dict(review):
    """Serialize a review object."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id,
        'place_id': review.place.id
    }


@api.route('/')
class ReviewList(Resource):
    """Endpoint for listing and creating reviews."""

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get list of all reviews."""
        reviews = facade.get_all_reviews()
        return [review_to_dict(r) for r in reviews], 200

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review."""
        try:
            review = facade.create_review(api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return review_to_dict(review), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Endpoint for getting, updating, and deleting a specific review."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review_to_dict(review), 200

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        try:
            updated = facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return review_to_dict(updated), 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Endpoint for getting reviews by place."""

    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [review_to_dict(r) for r in reviews], 200