from flask import request, jsonify

from util import get_logger
from util import right_just_dict
from web.flask import flask

log = get_logger(__name__)


@flask.route("/demo/hello", methods=["GET"])
def demo_hello():
    """Example with simple swagger definition
    This is the most simple swagger definition example.
    ---
    tags:
      - demo
    # tags: [demo1, demo3]
    parameters:
      - name: username
        in: query
        type: string
        required: true
      - name: age
        in: query
        type: integer
    responses:
      200:
        description: The person you called.
        schema:
          $ref: Person
    """
    info = {'Header[User-Agent]': request.headers.get('User-Agent'),
            'args': request.args,
            'query_string': request.query_string,
            'name': request.args.get('name')}
    log.info('Request Info:\n%s', right_just_dict(info))
    return jsonify(dict(rc=0, data=dict(id=2, username=request.args.get('username'), age=request.args.get('age', 23)), msg='success'))


@flask.route("/demo/colors/<string:palette>/", methods=["GET"])
def colors(palette):
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    tags: [demo]
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
      Person:
        type: object
        properties:
          name:
            type: string
          age:
            type: integer
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
      405:
        description: Invalid input 
        schema:
          $ref: Palette
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}
    return jsonify(result)

