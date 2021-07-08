import logging

from flask import request
from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh.business import create_playout
from cingerine.api.dooh.parsers import pagination_arguments
from cingerine.api.dooh.serializers import page_of_playouts, playoutPlan
from cingerine.api.restplus import api
from cingerine.database.models import PlayoutPlan

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/playouts', description='Operations related to playouts')


@ns.route('/')
class PlayOutCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_playouts)
    def get(self):
        """
        Returns list of playout plans.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        query = PlayoutPlan.query  # noqa

        all_ = list(query.all())
        page = query.paginate(page, per_page, error_out=False)

        return page

    @api.expect(playoutPlan)
    def post(self):
        """
        Registers a new playout plan
        Each combination of (player, asset, hour) overwrites any pre-existing targets or counts
        for that combination.
        """
        playout_id = create_playout(request.json)
        return {'playoutId': playout_id}, 201


@ns.route('/<int:playout_id>')
@api.response(404, 'Playout Plan not found.')
class PlayOutItem(Resource):

    @api.marshal_with(playoutPlan)
    def get(self, playout_id):
        """
        Returns a playout plan.
        """
        return PlayoutPlan.query.filter(PlayoutPlan.playoutId == playout_id).one()
