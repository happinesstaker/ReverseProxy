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
import pyfscache

NEXT_BUS_API_ENDPOINT = 'http://webservices.nextbus.com/service/'
SLOW_THRESH = 1.0 #unit: second
CACHE_EXPIRE = 5 #unit: minute

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

    if endpoint in cache_it:
        return cache_it[endpoint]

    start = time.time()
    res = requests.get(url, params=request.args)
    elapse = time.time() - start

    with lock:
        if elapse > SLOW_THRESH:
            slow_request_dict[endpoint] = "%.1fs" % elapse

    response = Response(res.content, res.status_code, [('Content-Type', res.headers['Content-Type'])])
    cache_it[endpoint] = response
    return response

@app.route("/stats")
def get_stat():
    # no need to lock when reading, it is OK to get obsolete stat data
    # of course we can also use rwlock, but let's simplify everything
    return jsonify({'slow_requests':slow_request_dict, 'queries':query_dict})

if __name__ == '__main__':
    if 'SLOW_THRESH' in os.environ:
        try:
            SLOW_THRESH = float(os.environ['SLOW_THRESH'])
            print "SLOW_THRESH set by config: %.1f seconds" % SLOW_THRESH
        except ValueError as e:
            print "Incompatible env var for SLOW_THRESH, use default value 1 second"

    if 'CACHE_EXPIRE' in os.environ:
        try:
            CACHE_EXPIRE = int(os.environ['CACHE_EXPIRE'])
            print "CACHE_EXPIRE set by config: %d minutes" % CACHE_EXPIRE
        except ValueError as e:
            print "Incompatible env var for CACHE_EXPIER, use default value 5 minutes"

    print "Reverse Proxy Started, Listening at Port 80..."
    cache_it = pyfscache.FSCache('cache', minutes=CACHE_EXPIRE)
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
