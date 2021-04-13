import json
import logging
import os
import uuid

from flask_restplus import Resource

from cingerine import settings
from cingerine.api.dooh import parsers
from cingerine.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace(f'{settings.API_VERSION}/assets', description='Operations related to video assets')


@ns.route('/')
class AssetsCollection(Resource):

    @api.expect(parsers.file_upload)
    def post(self):

        asset_id = str(uuid.uuid4())

        args = parsers.file_upload.parse_args()

        asset = f'{asset_id}.asset'
        image_file = args['content']
        destination = os.path.join(settings.UPLOAD_FOLDER, asset)
        if not os.path.exists(settings.UPLOAD_FOLDER):
            os.makedirs(settings.UPLOAD_FOLDER)
        image_file.save(destination)
        if image_file.mimetype and image_file.mimetype != 'video/mp4':
            return {"errors": [{"errorcode": "UNSUPPORTED_MIMETYPE",
                                "message": "We only support video/mp4"},
                               {"errorcode": "UNSUPPORTED_FILETYPE",
                                "message": "We only support mp4 files"}]}, 400
        metadata = f'{asset_id}.meta'
        with open(os.path.join(settings.UPLOAD_FOLDER, metadata), 'w') as file:
            file.write(args['metadata'])

        metadata_json = json.loads(args['metadata'])

        return {'cmsAssetId': asset_id,
                'name': destination,
                'metadata': metadata_json}, 201
