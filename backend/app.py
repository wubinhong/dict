from util import get_logger
from web.flask import flask
from web.setting import FLASK_PORT, FLASK_DEBUG

log = get_logger(__name__)


if __name__ == '__main__':
    # 启动接口服务
    from web.rest import filter, demo
    log.info('Import rest module: %s | %s', filter.__name__, demo.__name__)
    flask.run(host='0.0.0.0', port=FLASK_PORT, debug=FLASK_DEBUG)
