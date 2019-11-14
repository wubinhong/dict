import json
import time
from collections import OrderedDict

from flask import g, request, jsonify

from util.error import Error
from util import get_logger
from web.flask import flask

log = get_logger(__name__)


@flask.before_request
def log_request_before():
    g.request_start = time.time()


@flask.after_request
def log_request_info(response):
    # logger.debug('api access stats: \nHeaders: %20s', request.headers)
    headers = request.headers
    content_type = response.content_type
    if content_type and content_type.find('application/json') != -1:
        stats_info = OrderedDict()
        stats_info['from'] = request.remote_addr
        stats_info['req'] = '%s %s' % (request.method, request.path)
        stats_info['req_query'] = request.query_string
        stats_info['req_args'] = request.args
        stats_info['req_body'] = request.get_data()
        stats_info['x-tianchi-client'] = headers.get('x-tianchi-client')
        stats_info['x-tianchi-token'] = headers.get('x-tianchi-token')
        stats_info['User-Agent'] = headers.get('User-Agent')
        stats_info['Content-Type'] = content_type
        stats_info['status'] = response.status
        stats_info['time_cost'] = time.time() - g.request_start
        try:
            stats_info['res'] = json.loads(str(response.data, 'utf-8'))
        except ValueError:
            stats_info['res'] = response.data

        log.info('api access stats: \nAccess Detail Stats: \n%s%s\n', pretty_map(stats_info), '-' * 50)
    return response


def pretty_map(stats_map):
    map_2_str = ''
    for k, v in stats_map.items():
        map_2_str += '%20s : %s\n' % (k, v)
    return map_2_str


@flask.errorhandler(Error)
def error(err):
    log.exception(err)
    log.warning('custom error: %s', repr(err))
    return jsonify(dict(code=err.code, msg=err.msg))


@flask.errorhandler(500)
def error(err):
    log.exception(err)
    log.error('system error: %s', err)
    return jsonify(dict(code=50000, msg='Internal Server Error!')), 500
