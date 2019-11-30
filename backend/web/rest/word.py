from flask import request, jsonify, make_response

from web.util import get_logger
from web.flask import flask
from web.model import words

log = get_logger(__name__)


@flask.route("/words/fuzzy", methods=["GET"])
def get_words_fuzzy():
    """Get word list with fuzzy matching
    Sorted by field updated_at
    ---
    tags: [word]
    definitions:
      Word:
        type: object
        properties:
          name:
            type: string
            description: 单词
          derivation:
            type: string
            description: 词根组成，如：a+scend
          chinese:
            type: string
            description: 中文解释，多种解释使用逗号（,）分隔
          thesauri:
            type: string
            description: 同义词，使用逗号（,）分隔
          related_words:
            type: string
            description: 相关单词，使用逗号（,）分隔
          similar_shaped_words:
            type: string
            description: 形状相识的单词，使用逗号（,）分隔
          comment:
            type: string
            description: 其他备注
          created_at:
            type: datetime
            description: 单词录入时间
          created_at:
            type: datetime
            description: 单词最近一次更新（修订）的时间
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
        description: Words fuzzy matched.
        schema:
          $ref: '#/definitions/Word'
    """
    keyword = request.args.get('keyword')
    skip = request.args.get('skip', type=int)
    limit = request.args.get('limit', type=int)
    resp = make_response(jsonify(dict(rc=0, data=words.find_fuzzy(keyword, skip, limit), msg='success')))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@flask.route("/words/<string:name>", methods=["GET"])
def get_word_by_name(name):
    """Get word detail by name
    As title
    ---
    tags: [word]
    parameters:
      - name: name
        description: 单词名字
        in: path
        type: string
        required: true
    responses:
      200:
        description: Word matched.
        schema:
          $ref: '#/definitions/Word'
    """
    return jsonify(dict(rc=0, data=words.find_by_name(name), msg='success'))


@flask.route("/words/<string:name>", methods=["PUT"])
def put_word(name):
    """Save word and update if exits
    As title
    ---
    tags: [word]
    parameters:
      - name: name
        description: 单词名字
        in: path
        type: string
        required: true
      - name: req
        description: stored in the playload  with json format and field name will be place by path parameter above.
        in: body
        type: json
        required: true
        schema:
          $ref: '#/definitions/Word'
    responses:
      200:
        description: updated word.
        schema:
          $ref: '#/definitions/Word'
    """
    w = request.json
    log.info('Put word: %s | %s', name, w)
    return jsonify(dict(rc=0, data=words.save(w), msg='success'))


@flask.route("/words/<string:name>", methods=["DELETE"])
def delete_word(name):
    """Delete word by name
    As title
    ---
    definitions:
      MongoRawResult:
        type: object
        properties:
          n:
            type: integer
            description: The count of affected documents
          ok:
            type: integer
            description: 1 for success
    tags: [word]
    parameters:
      - name: name
        description: 单词名字
        in: path
        type: string
        required: true
    responses:
      200:
        description: Delete word.
        schema:
          $ref: '#/definitions/MongoRawResult'
    """
    return jsonify(dict(rc=0, data=words.delete_by_name(name), msg='success'))
