import logging

from flask import request
from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh.business import create_player
from cingerine.api.dooh.parsers import pagination_arguments
from cingerine.api.dooh.serializers import page_of_players, player, playerState
from cingerine.api.restplus import api
from cingerine.database import db
from cingerine.database.models import Player, PlayerState
import datetime as dt

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/players', description='Operations related to player inventory')


@ns.route('/dev/reset')
class DevSupport(Resource):

    def delete(self):
        log.info("resetting DB")
        num_rows = db.session.query(Player).delete()
        db.session.commit()
        log.info(f"Deleted {num_rows if num_rows else 'no'} row{'s' if num_rows > 1 else ''}")
        return None, 200


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


@ns.route('/<int:player_id>')
@api.response(404, 'Player not found.')
class PlayerItem(Resource):

    @api.marshal_with(player)
    def get(self, player_id):
        """
        Returns a player.
        """
        return Player.query.get_or_404(player_id)


@ns.route('/<int:player_id>/health')
@api.response(404, 'No such player.')
class PlayerItem(Resource):

    @api.marshal_with(playerState)
    def get(self, player_id):
        """
        Returns a the current state of the given player
        """
        the_player = Player.query.filter(Player.playerId == player_id).one()

        return PlayerState(playerId=the_player.playerId, playerState='running',
                           lastActive=dt.datetime.now().isoformat('T', 'seconds'))
