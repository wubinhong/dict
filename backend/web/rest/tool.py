from flask import request, jsonify, make_response

from web.util import get_logger, make_msg
from web.flask import flask
from web.model import histories

log = get_logger(__name__)


@flask.route("/api/tool/histories/fuzzy", methods=["GET"])
def get_history_fuzzy():
    """Get history list with fuzzy matching
    Sorted by field updated_at
    ---
    tags: [tool]
    definitions:
      History:
        type: object
        description: 工具历史记录
        properties:
          title:
            type: string
            description: 历史的标题，推荐使用日期字符串，相同的标题则会覆盖内容
          content:
            type: string
            description: 历史对应的内容
          created_at:
            type: datetime
            description: 创建时间
          updated_at:
            type: datetime
            description: 最近一次更新（修订）的时间
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
        description: History fuzzy matched.
        schema:
          $ref: '#/definitions/History'
    """
    keyword = request.args.get('keyword')
    skip = request.args.get('skip', type=int)
    limit = request.args.get('limit', type=int)
    return jsonify(make_msg(data=histories.find_fuzzy(keyword, skip, limit)))


@flask.route("/api/tool/histories", methods=["PUT"])
def put_history():
    """Save history and update if exits
    As title
    ---
    tags: [tool]
    parameters:
      - name: req
        description: stored in the playload  with json format.
        in: body
        type: json
        required: true
        schema:
          $ref: '#/definitions/History'
    responses:
      200:
        description: updated history.
        schema:
          $ref: '#/definitions/History'
    """
    body = request.json
    log.info('Put History: %s', body)
    return jsonify(make_msg(data=histories.save_by_title(body)))


@flask.route("/api/tool/history/<string:_id>", methods=["DELETE"])
def delete_history(_id):
    """Delete history by id
    As title
    ---
    tags: [tool]
    parameters:
      - name: id
        description: 历史id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Delete history.
        schema:
          $ref: '#/definitions/MongoRawResult'
    """
    return jsonify(make_msg(data=histories.delete_by_id(_id)))


@flask.route("/api/tool/history/<string:_id>", methods=["GET"])
def get_history_by_id(_id):
    """Get history by id
    ---
    tags: [tool]
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: History matched.
        schema:
          $ref: '#/definitions/History'
    """
    return jsonify(make_msg(data=histories.find_by_id(_id)))
