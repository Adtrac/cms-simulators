import logging.config
import os

from flask import Flask, Blueprint
from flask_migrate import Migrate


from cingerine import settings
from cingerine.database import db
from cingerine.api.dooh.endpoints.categories import ns as blog_categories_namespace
from cingerine.api.dooh.endpoints.players import ns as players_namespace
from cingerine.api.dooh.endpoints.posts import ns as blog_posts_namespace
from cingerine.api.dooh.endpoints.assets import ns as assets_namespace
from cingerine.api.restplus import api

migrate = Migrate()


logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    # flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app():

    app = create_app()

    log.info("Initializinig DB:")
    db.init_app(app)
    migrate.init_app(app, db)
    log.info("Done.")

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    api.add_namespace(players_namespace)
    api.add_namespace(assets_namespace)
    app.register_blueprint(blueprint)

    return app


def main():
    app = initialize_app()
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
