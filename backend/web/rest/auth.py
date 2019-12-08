from flask import jsonify, request

from web.flask import flask
from web.model import admins
from web.util import get_logger, make_msg

log = get_logger(__name__)


@flask.route("/api/auth/login", methods=["POST"])
def login():
    """Login
    As title
    ---
    tags: [auth]
    definitions:
      Auth:
        type: object
        description: 登录
        properties:
          name:
            type: string
            description: 用户名
          password:
            type: string
            description: 密码
    parameters:
      - name: req
        description: stored in the playload  with json format.
        in: body
        type: json
        required: true
        schema:
          $ref: '#/definitions/Auth'
    responses:
      200:
        description: Login success
        schema:
          $ref: '#/definitions/Admin'
    """
    name = request.json.get('name')
    password = request.json.get('password')
    log.info('Admin login: %s | %s', name, password)
    return jsonify(make_msg(data=admins.login(name, password), msg='登录成功！'))


@flask.route("/api/auth/logout", methods=["DELETE"])
def logout():
    """Lout
    As title
    ---
    tags: [auth]
    parameters:
      - name: x-hucat-token
        description: 放在请求头的令牌
        in: header
        type: String
        required: true
    responses:
      200:
        description: Logout success
    """
    return jsonify(make_msg(data=admins.logout(request.headers.get('x-hucat-token')), msg='登录成功！'))
