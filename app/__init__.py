import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.celery.celery import NotifyCelery
from cubes import Workspace


migrate = Migrate()
db = SQLAlchemy()
notify_celery = NotifyCelery()
notify_workspace = Workspace()


def create_app(application):

    from app.config import configs

    notify_environment = os.environ['NOTIFY_ENVIRONMENT']

    application.config.from_object(configs[notify_environment])

    # init_app(application)
    notify_celery.init_app(application)

    db.init_app(application)
    migrate.init_app(application, db=db)
    register_blueprint(application)

    return application


def create_slicer_config():
    import configparser
    config = configparser.ConfigParser()

    config['server'] = {
                        # 'host': 'localhost',
                        # 'port': os.environ['PORT'], # no need check port number when run using flask run
                        'reload': 'yes',
                        'log_level': 'info',
                        'authentication': 'http_basic_proxy'}

    config['workspace'] = {'models_path': './app',
                        'log_level': 'debug'}
    config['model'] = {'path': 'model.json'}
    config['store'] = {'type': 'sql',
                        'schema': 'public',
                        'username': 'name',     # TODO: Replace with secret from OS
                        'password': 'pass',     # TODO: Replace with secret from OS
                        'url': os.environ['SQLALCHEMY_DATABASE_URI']}
    return config


def create_slicer(application):
    from app.config import configs
    from cubes.server.base import run_server, create_server

    config = create_slicer_config()

    application = create_server(config)
    return application


def register_blueprint(application):
    from app.rest.test import test_blueprint
    from app.cubes_browser.rest import cubes_blueprint
    from cubes.server import slicer
    from cubes.compat import ConfigParser

    notify_workspace.register_default_store("sql", url="postgresql://venusbailey@localhost:5432/notify_reports",
                                            schema="public")
    notify_workspace.import_model("app/model.json")

    # updating_blueprint.before_request()
    application.register_blueprint(test_blueprint)
    application.register_blueprint(cubes_blueprint)

    # Slice server
    settings = ConfigParser()
    settings.read("slicer.ini")
    application.register_blueprint(slicer, url_prefix="/slicer", config=settings)

    # This is an example app
    @application.route('/get_data_by_year')
    def get_data():
        browser = notify_workspace.browser("ft_billing")
        cube = browser.cube
        result = browser.aggregate(drilldown=["dm_datetime:year"])
        return_str = ''
        for record in result:
            return_str = return_str + str(record) + '<br>'
        return return_str



