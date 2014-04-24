#!/bin/bash

while :; 
do
    locust --no-web -c 10 -r 1 -L CRITICAL & PROC=$1; sleep 0.1; kill $!
done
#locust --no-web -c 100 -r 100 -L INFO -r2
#locust --no-web -c 100 -r 100 -L INFO -r2

# EOF
