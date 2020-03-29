from collections import OrderedDict
from os import environ

from web.util import get_logger, right_just_dict

log = get_logger(__name__)

# http server setting
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

MONGO_URI = 'mongodb://root:123456@127.0.0.1:27017/dict'
REDIS_OPTS = {
    'host': '127.0.0.1', 'port': 6379, 'password': None, 'socket_connect_timeout': 8, 'decode_responses': True
}
AUTH_TOKEN_PREFIX = 'auth_token_'
# swagger settings
# swagger docs default access url: http://localhost:5000/apidocs/
SWAGGER = {
    'title': 'My API',
    'uiversion': 2,
    'securityDefinitions': {
        'token': {
            'type': 'apiKey', 'in': 'header', 'name': 'x-hucat-token'
        }
    }
}

mode = environ.get('PYTHON_ENV')
mode = mode if mode else 'local'

if mode == 'product':
    FLASK_DEBUG = False
    MONGO_URI = 'mongodb://127.0.0.1:27017/dict'

log.info('Setting Info:\n%s' % right_just_dict(
    OrderedDict(mode=mode, FLASK_PORT=FLASK_PORT, FLASK_DEBUG=FLASK_DEBUG, MONGO_URI=MONGO_URI,
                SWAGGER_DOCS='http://{0}:{1}/apidocs/'.format(FLASK_HOST, FLASK_PORT))))
