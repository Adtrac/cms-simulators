import werkzeug
from flask_restplus import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')

file_upload = reqparse.RequestParser()
file_upload.add_argument('video',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='image')
file_upload.add_argument('fileName',
                         type=str, required=True, help='base name.')
