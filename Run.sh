#!/bin/sh

docker run -d -e SLOW_THRESH=0.2 -e CACHE_EXPIRE=3 -p 8080:80 reverse_proxy
