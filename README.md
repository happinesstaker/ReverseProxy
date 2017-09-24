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
* cache expiration time

I use environment variable when running docker application to pass in arguments