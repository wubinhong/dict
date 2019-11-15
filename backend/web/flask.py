import datetime
import json

from bson.objectid import ObjectId
from flasgger import Swagger
from flask import Flask
from pymongo import MongoClient

from web.util import get_logger
from web.setting import MONGO_URI

log = get_logger(__name__)
flask = Flask(__name__)
flask.config.from_object("web.setting")
# swagger configuration see web.setting, for more info: https://github.com/flasgger/flasgger
# swagger yml definition: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#parameterObject
swagger = Swagger(flask)

# pymongo
dict_db = MongoClient(MONGO_URI, tz_aware=True)['dict']


class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
flask.json_encoder = JSONEncoder
