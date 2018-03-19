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


def create_cubes_config():
    import configparser
    config = configparser.ConfigParser()

    config['server'] = {
                        # 'host': 'localhost',
                        # 'port': os.environ['PORT'], # no need check port number when run using flask run
                        'reload': 'yes',
                        'log_level': 'info'}
    config['workspace'] = {'models_path': './app',
                        'log_level': 'debug'}
    config['model'] = {'path': 'model.json'}
    config['store'] = {'type': 'sql',
                        'schema': 'public',
                        'url': os.environ['SQLALCHEMY_DATABASE_URI']}
    return config


def create_slicer():
    from app.config import configs
    from cubes.server.base import run_server, create_server

    config = create_slicer_config()

    application = create_server(config)
    return application



def register_blueprint(application):
    from app.rest.test import test_blueprint
    from app.cubes_browser.rest import cubes_blueprint
    # from cubes.server import slicer
    # from cubes.compat import ConfigParser

    notify_workspace.register_default_store("sql", url=os.environ['SQLALCHEMY_DATABASE_URI'],
                                            schema="public")
    notify_workspace.import_model("app/model.json")

    # updating_blueprint.before_request()
    application.register_blueprint(test_blueprint)
    application.register_blueprint(cubes_blueprint, url_prefix='/cubes')

    # Slice server
    # settings = ConfigParser()
    # settings.read("slicer.ini")
    # config=create_cubes_config()
    # application.register_blueprint(slicer, url_prefix="/slicer", config=config)

    # This is an example app
    from flask import request
    @application.route('/get_data_by_year', methods=['GET', 'POST'])
    def get_data():
        if 'drilldown' in request.args:
          drilldown = request.args.get('drilldown')
        else:
          drilldown = 'month'
        browser = notify_workspace.browser("ft_billing")
        cube = browser.cube
        result = browser.aggregate(drilldown=["dm_datetime:{}".format(drilldown)])
        return_str = ''
        for record in result:
            return_str = return_str + str(record) + '<br>'
        return return_str



