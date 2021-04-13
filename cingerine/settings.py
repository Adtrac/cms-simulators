import tempfile

# Flask settings
FLASK_SERVER_NAME = 'localhost:8882'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True

API_VERSION = 'v1_1'
UPLOAD_FOLDER = 'UPLOADS'
DATA_FOLDER = tempfile.gettempdir()

URL_PREFIX = '/api/dooh'
