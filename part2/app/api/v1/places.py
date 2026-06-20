"""Place endpoints for HBnB API."""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})


def place_to_dict(place):
    """Serialize a place object."""
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        },
        'amenities': [{'id': a.id, 'name': a.name}
                      for a in place.amenities]
    }


@api.route('/')
class PlaceList(Resource):
    """Endpoint for listing and creating places."""

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get list of all places."""
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title,
                 'latitude': p.latitude,
                 'longitude': p.longitude} for p in places], 200

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place."""
        try:
            place = facade.create_place(api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return place_to_dict(place), 201


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Endpoint for getting and updating a specific place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place_to_dict(place), 200

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            updated = facade.update_place(place_id, api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return place_to_dict(updated), 200