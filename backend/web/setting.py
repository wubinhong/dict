from collections import OrderedDict
from os import environ

from util import get_logger, right_just_dict

log = get_logger(__name__)

# http server setting
FLASK_DEBUG = True
FLASK_PORT = 5000
mongodb_uri = 'mongodb://127.0.0.1:27017/dict'
# swagger settings
# swagger docs default access url: http://localhost:5000/apidocs
SWAGGER = {
    'title': 'My API',
    'uiversion': 2
}

mode = environ.get('PYTHON_ENV')
mode = mode if mode else 'local'

if mode == 'product':
    DEBUG = False
    mongodb_uri = 'mongodb://root:123456@mongodb.backend.com:27017/dict'

log.info('Setting Info:\n%s' % right_just_dict(
    OrderedDict(mode=mode, FLASK_PORT=FLASK_PORT, FLASK_DEBUG=FLASK_DEBUG, mongodb_uri=mongodb_uri)))

