import logging

from flask import request
from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh.business import create_player, update_player, delete_player
from cingerine.api.dooh.parsers import pagination_arguments
from cingerine.api.dooh.serializers import page_of_players, player, player_with_opening_hours
from cingerine.api.restplus import api
from cingerine.database.models import Player

log = logging.getLogger(__name__)

ns = api.namespace(f'dooh/{settings.API_VERSION}/players', description='Operations related to player inventory')


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


@ns.route('/<string:playerId>')
@api.response(404, 'Player not found.')
class PlayerItem(Resource):

    @api.marshal_with(player_with_opening_hours)
    def get(self, playerId):
        """
        Returns a particular player
        """
        return Player.query.filter(Player.playerId == playerId).one()

    @api.expect(player)
    @api.response(204, 'Player successfully updated.')
    def put(self, playerId):
        """
        Updates a player.
        """
        data = request.json
        update_player(playerId, data)
        return None, 204

    @api.response(204, 'Player successfully deleted.')
    def delete(self, playerId):
        """
        Deletes a player
        """
        delete_player(playerId)
        return None, 204
