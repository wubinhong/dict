from web.util import get_logger
from web.flask import flask
from web.setting import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

log = get_logger(__name__)

if __name__ == '__main__':
    # 启动接口服务
    from web.rest import filter, demo, word, admin, tool, auth
    log.info('Import rest module: %s | %s | %s', filter.__name__, demo.__name__, word.__name__)
    flask.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
