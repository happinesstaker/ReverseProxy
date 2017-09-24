'''
Written by: Jiajie YANG <happinesstaker@gmail.com>
Interesting coding challenge to build a reverse proxy towards NextBus.
'''

from collections import defaultdict
from urlparse import urlparse
from threading import Lock
import time
import os

from flask import Flask, request, Response, jsonify
import requests


NEXT_BUS_API_ENDPOINT = 'http://webservices.nextbus.com/service/'
SLOW_THRESH = 1.0 #unit: second


app = Flask(__name__)

slow_request_dict = defaultdict(str)
query_dict = defaultdict(int)
lock = Lock()

@app.route("/service/<path:query>")
def dispatch(query):
    url = NEXT_BUS_API_ENDPOINT + query
    endpoint = request.query_string

    with lock:
        query_dict[endpoint] += 1

    start = time.time()
    res = requests.get(url, params=request.args)
    elapse = time.time() - start

    with lock:
        if elapse > SLOW_THRESH:
            slow_request_dict[endpoint] = "%.1fs" % elapse

    return Response(res.content, res.status_code, [('Content-Type', res.headers['Content-Type'])])

@app.route("/stats")
def get_stat():
    # no need to lock when reading, it is OK to get obsolete stat data
    # of course we can also use rwlock, but let's simplify everything
    return jsonify({'slow_requests':slow_request_dict, 'queries':query_dict})

if __name__ == '__main__':
    if 'SLOW_THRESH' in os.environ:
        try:
            SLOW_THRESH = float(os.environ['SLOW_THRESH'])
            print "SLOW_THRESH set by config: %.1f" % SLOW_THRESH
        except ValueError as e:
            print "Incompatible env var for SLOW_THRESH, please use float (seconds) for it"

    print "Reverse Proxy Started, Listening at Port 80..."
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
