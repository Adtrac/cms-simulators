import logging

from flask import request
from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh.business import create_player
from cingerine.api.dooh.parsers import pagination_arguments
from cingerine.api.dooh.serializers import page_of_players, player
from cingerine.api.restplus import api
from cingerine.database.models import Player

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/players', description='Operations related to player inventory')


@ns.route('/')
class PlayersCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_players)
    def get(self):
        """
        Returns list of players.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        query = Player.query  # noqa
        page = query.paginate(page, per_page, error_out=False)

        return page

    @api.expect(player)
    def post(self):
        """
        Registers a new player
        """
        create_player(request.json)
        return None, 201
