import werkzeug
from flask_restplus import reqparse


pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')

report_arguments = reqparse.RequestParser()
report_arguments.add_argument('start', type=str, required=True, help='First reported day')
report_arguments.add_argument('end', type=str, required=True, help='Last reported day')
report_arguments.add_argument('assets', type=str, action='split',
                              required=True, help='Ids of the asset to report for.')


file_upload = reqparse.RequestParser()
file_upload.add_argument('content', type=werkzeug.datastructures.FileStorage,
                         location='files', required=False, help='This is the content')

file_upload.add_argument('metadata', help='Arbitrary JSON')
