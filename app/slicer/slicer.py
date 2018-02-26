import configparser
from cubes import Workspace
from flask import current_app


def create_config(application):
    config = configparser.ConfigParser()
    config['server'] = {'host': 'localhost',
                        'port': str(application.config.get('SLICER_PORT')),
                        'reload': 'yes',
                        'log_level': 'info',
                        'authentication': 'http_basic_proxy'}

    config['workspace'] = {'models_path': '.',
                        'log_level': 'debug'}
    config['model'] = {'path': 'model.json'}
    config['store'] = {'type': 'sql',
                        'schema': 'public',
                        'username': 'name',     # TODO: Replace with secret from OS
                        'password': 'pass',     # TODO: Replace with secret from OS
                        'url': str(application.config.get('SQLALCHEMY_DATABASE_URI'))}
    return config



# def start_slicer():
#     # execute only if run as a script
#     config = create_config()
#     run_server(config=config, debug=True)