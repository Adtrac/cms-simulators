import logging
import os

from flask_restplus import Resource, abort

from cingerine import settings
from cingerine.api.dooh import parsers
from cingerine.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/assets', description='Operations related to video assets')


@ns.route('/')
class AssetsCollection(Resource):

    @api.expect(parsers.file_upload)
    def post(self):

        # none of the below is working yet

        args = parsers.file_upload.parse_args()
        if args['video'].mimetype != 'video/mp4':
            abort(404)

        video_file = args['video']
        filename = args['fileName']

        destination = os.path.join(settings.DATA_FOLDER, 'videos')

        if not os.path.exists(destination):
            os.makedirs(destination)

        full_path = os.path.join(destination, filename)
        video_file.save(full_path)

        return {'status': 'Done'}
