from flask import Flask, jsonify
from datetime import datetime
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def hello_world():
    ret = dict(msg='Hello, World!', ts=datetime.now().timestamp())
    print(ret)
    return jsonify(ret)

# Only for development
# app.run('0.0.0.0', 8000)

# gevent Container - showed the highest performance, with throughput roughly 2541 req/sec.
http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()

# Twisted: A mature, non-blocking event-driven networking library. Throughput was roughly 600 req/sec.
"""
$ pip3 install Twisted
$ twistd web --port tcp:8000 --wsgi flask_server.app
"""

# gunicorn - Throughput was roughly 800 req/sec.
"""
$ pip3 install gunicorn
$ gunicorn -w 4 -b 127.0.0.1:8000 flask_server:app
"""