##!/usr/bin/env python
from __future__ import print_function

from flask import Flask

from app import create_slicer


# application = Flask('app')

application = create_slicer()


# from cubes.server.blueprint import slicer
# config = create_slicer_config()
# application.register_blueprint(slicer, config=config)