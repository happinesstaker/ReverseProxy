#!/bin/sh

echo "Test Single Access"
echo "=================="
curl '127.0.0.1/service/publicXMLFeed?command=agencyList' | head

echo "\n"
echo "Test Burst Access (100)"
echo "======================="
for i in {1..100}
do
    curl '127.0.0.1/service/publicXMLFeed?command=agencyList' &> /dev/null
    printf "."
done
echo "Ended\n"

echo "Stat"
curl '127.0.0.1/stats'

# it is possible to traverse through xml and do further query, but that takes much time
