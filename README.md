## Reverse Proxy Towards NextBus

I choose to use Flask as it is light-weight and support multi-threaded service for clients, which meet the requirements specified

### Main Functionality:

* dispatch traffic towards NextBus
* collect statistic of slow connection / endpoint visiting counter and expose API for this statistics (however, since there is only 1 valid endpoint in NextBus API, we use query params in GET request as our stats endpoint)

### Endpoints for functionality:

* <host>/service/[query] -> dispatch to NextBus
* <host>/stats -> return json formatted statistics for reverse proxy

*Assume all API requests in NextBus starts at /services/publicXMLFeed?command=CMD&... as stated in the pdf instruction for it*

*Assume slow request stat would only keep the last time count of that endpoint which exceeds threshold*

### Configurable Arguments

* Slow request time shreshold (in seconds) default 0.5s
* cache expiration time (in minutes) default 5 minutes

I use environment variable when running docker application to pass in arguments

### Cache Layer

There is existing library to cache data on disk with expiration, I just use that library to achieve this effect. If I would to implement by myself, I would create cache file and spawn a thread to unlink it when timer expires.

### Scalable Web Service

I used docker compose to let my reverse proxy horizontally scalable, and add a HAProxy application as the front-end load balancer to dispatch traffic towards each reverse proxy application

### Database Storage

Since the size of data we want to store is quite small, and its nature is statistics for running status for all proxy application, keep a in-memory, light-weight database storage is quite enough, so I choose Redis to incur minimum code modification