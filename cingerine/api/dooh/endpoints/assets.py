import logging
import os

import werkzeug
from flask_restplus import Resource, abort, reqparse

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

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("your_file_name.jpg")


        args = parsers.file_upload.parse_args()
        if args['xls_file'].mimetype == 'application/xls':
            destination = os.path.join(settings.DATA_FOLDER, 'medias')
            if not os.path.exists(destination):
                os.makedirs(destination)
            xls_file = '%s%s' % (destination, 'custom_file_name.xls')
            args['xls_file'].save(xls_file)
        else:
            abort(404)
        return {'status': 'Done'}
