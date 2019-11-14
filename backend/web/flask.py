from flasgger import Swagger
from flask import Flask

from util import get_logger

log = get_logger(__name__)
flask = Flask(__name__)
flask.config.from_object("web.setting")
# swagger configuration see web.setting, for more info: https://github.com/flasgger/flasgger
# swagger yml definition: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#parameterObject
swagger = Swagger(flask)
