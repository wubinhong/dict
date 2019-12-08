import json
import time
from collections import OrderedDict
import re

from flask import g, request, jsonify

from web.util.error import Error
from web.setting import AUTH_TOKEN_PREFIX
from web.util import get_logger, make_msg
from web.flask import flask, redis

log = get_logger(__name__)
auth_regexp = re.compile(r'^/api/[\w\-/.]+')
auth_exempt_regexp = re.compile(r'^/api/auth/[\w\-/.]+')


def auth_request(path):
    return auth_regexp.match(path) and not auth_exempt_regexp.match(path)


@flask.before_request
def log_request_before():
    g.request_start = time.time()
    if auth_request(request.path):
        token = request.headers.get('x-hucat-token')
        if not token:
            raise Error(10000)
        if not redis.get(AUTH_TOKEN_PREFIX + token):
            log.warn('No result matched for token in redis: %s', AUTH_TOKEN_PREFIX + token)
            raise Error(10001)


@flask.after_request
def log_request_info(response):
    # logger.debug('api access stats: \nHeaders: %20s', request.headers)
    headers = request.headers
    content_type = response.content_type
    if auth_request(request.path) and content_type and content_type.find('application/json') != -1:
        stats_info = OrderedDict()
        stats_info['from'] = request.remote_addr
        stats_info['req'] = '%s %s' % (request.method, request.path)
        stats_info['req_query'] = request.query_string
        stats_info['req_args'] = request.args
        stats_info['req_body'] = request.get_data()
        stats_info['x-hucat-client'] = headers.get('x-hucat-client')
        stats_info['x-hucat-token'] = headers.get('x-hucat-token')
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
    return jsonify(make_msg(rc=err.rc, msg=err.msg))


@flask.errorhandler(500)
def error(err):
    log.exception(err)
    log.error('system error: %s', err)
    return jsonify(make_msg(rc=50000, msg='Internal Server Error!')), 500
