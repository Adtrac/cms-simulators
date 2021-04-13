import logging

from flask import request
from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh.business import create_playout
from cingerine.api.dooh.parsers import pagination_arguments, report_arguments
from cingerine.api.dooh.serializers import playoutPlan, list_of_counts
from cingerine.api.restplus import api
from cingerine.database.models import ReportItem

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/reports', description='Operations related to reports')


@ns.route('/')
class ReportCollection(Resource):

    @api.expect(report_arguments)
    # @api.marshal_with(list_of_counts)
    def get(self):
        """
        Returns list of play out counts.
        """
        args = report_arguments.parse_args(request)
        start = args.get('start')
        end = args.get('end')
        assets = args.get('assets')

        query = ReportItem.query  # noqa

        all_ = list(query.all())

        return [
                   ['asset', 'player', '2021-04-10', 6, 10],
                   ['asset', 'player', '2021-04-10', 6, 10],
                   ['asset', 'player', '2021-04-10', 6, 10],
                   ['asset', 'player', '2021-04-10', 6, 10],
                   ['asset', 'player', '2021-04-10', 6, 10],
                   ['asset', 'player', '2021-04-10', 6, 10],
               ], 200

    @api.expect(playoutPlan)
    def post(self):
        """
        Registers a new playout
        """
        playout_id = create_playout(request.json)
        return {'playoutId': playout_id}, 201


@ns.route('/<int:playout_id>')
@api.response(404, 'Playout not found.')
class PlayOutItem(Resource):

    @api.marshal_with(playoutPlan)
    def get(self, playout_id):
        """
        Returns a player.
        """
        return PlayoutPlan.query.filter(PlayoutPlan.playoutId == playout_id).one()
