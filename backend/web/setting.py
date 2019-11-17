from collections import OrderedDict
from os import environ

from web.util import get_logger, right_just_dict

log = get_logger(__name__)

# http server setting
FLASK_DEBUG = True
FLASK_PORT = 5000

MONGO_URI = 'mongodb://root:123456@127.0.0.1:27017/dict'
# swagger settings
# swagger docs default access url: http://localhost:5000/apidocs
SWAGGER = {
    'title': 'My API',
    'uiversion': 2
}

mode = environ.get('PYTHON_ENV')
mode = mode if mode else 'local'

if mode == 'product':
    FLASK_DEBUG = False
    MONGO_URI = 'mongodb://127.0.0.1:27017/dict'

log.info('Setting Info:\n%s' % right_just_dict(
    OrderedDict(mode=mode, FLASK_PORT=FLASK_PORT, FLASK_DEBUG=FLASK_DEBUG, MONGO_URI=MONGO_URI)))
