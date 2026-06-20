"""Amenity endpoints for HBnB API."""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Endpoint for listing and creating amenities."""

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get list of all amenities."""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity."""
        try:
            amenity = facade.create_amenity(api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'id': amenity.id, 'name': amenity.name}, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Endpoint for getting and updating a specific amenity."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'id': updated.id, 'name': updated.name}, 200