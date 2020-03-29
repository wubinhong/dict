from flask import request, jsonify

from web.flask import flask
from web.model import admins
from web.util import get_logger, make_msg

log = get_logger(__name__)


@flask.route("/api/admins/fuzzy", methods=["GET"])
def get_admin_fuzzy():
    """Get admin list with fuzzy matching
    Sorted by field updated_at
    ---
    tags: [admin]
    definitions:
      Admin:
        type: object
        description: 管理员
        properties:
          name:
            type: string
            description: 用户名
          new_password:
            type: string
            description: 密码，重置密码可以用该字段
          salt:
            type: string
            description: 密码盐（加密用，一般不会返回）
          password:
            type: string
            description: 密码（new_password + salt -> password，加密后的密码，也不会返回）
          nick:
            type: string
            description: 昵称
          token:
            type: string
            description: 最近一次登录的token
          login_time:
            type: string
            description: 最近一次登录时间
          created_at:
            type: datetime
            description: 管理员创建时间
          updated_at:
            type: datetime
            description: 管理员最近一次更新（修订）的时间
    parameters:
      - name: keyword
        in: query
        type: string
        required: true
      - name: skip
        in: query
        type: integer
        required: true
      - name: limit
        in: query
        type: integer
        required: true
    responses:
      200:
        description: Admins fuzzy matched.
        schema:
          $ref: '#/definitions/Admin'
    """
    keyword = request.args.get('keyword')
    skip = request.args.get('skip', type=int)
    limit = request.args.get('limit', type=int)
    return jsonify(make_msg(data=admins.find_fuzzy(keyword, skip, limit)))


@flask.route("/api/admins", methods=["PUT"])
def put_admin():
    """Save admin and update if exits
    As title
    ---
    tags: [admin]
    parameters:
      - name: req
        description: stored in the playload  with json format.
        in: body
        type: json
        required: true
        schema:
          $ref: '#/definitions/Admin'
    responses:
      200:
        description: updated admin.
        schema:
          $ref: '#/definitions/Admin'
    """
    body = request.json
    log.info('Put admin: %s', body)
    return jsonify(make_msg(data=admins.save_by_name(body)))


@flask.route("/api/admins/<string:_id>", methods=["DELETE"])
def delete_admin(_id):
    """Delete admin by id
    As title
    ---
    tags: [admin]
    parameters:
      - name: id
        description: 管理员的id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Delete word.
        schema:
          $ref: '#/definitions/MongoRawResult'
    """
    return jsonify(make_msg(data=admins.delete_by_id(_id)))


@flask.route("/api/admins/<string:_id>", methods=["GET"])
def get_admin_by_id(_id):
    """Get admin by id
    ---
    tags: [admin]
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Admin matched.
        schema:
          $ref: '#/definitions/Admin'
    """
    return jsonify(make_msg(data=admins.find_by_id(_id)))
