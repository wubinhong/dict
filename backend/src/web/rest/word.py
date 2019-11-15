from flask import request, jsonify

from util import get_logger
from web.flask import flask
from web.model import words

log = get_logger(__name__)


@flask.route("/words/fuzzy", methods=["GET"])
def get_words_fuzzy():
    """Get word list with fuzzy matching
    As title
    ---
    tags: [word]
    definitions:
      Word:
        type: object
        properties:
          name:
            type: string
          derivation:
            type: string
          chinese:
            type: string
          thesauri:
            type: string
          related_words:
            type: string
          similar_shaped_words:
            type: string
          created_at:
            type: datetime
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
    return jsonify(dict(rc=0, data=words.find_fuzzy(keyword, skip, limit), msg='success'))


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
    data = words.save(name, derivation=w.get('derivation'), chinese=w.get('chinese'), thesauri=w.get('thesauri'),
               related_words=w.get('related_words'), similar_shaped_words=w.get('similar_shaped_words'))
    return jsonify(dict(rc=0, data=data, msg='success'))
