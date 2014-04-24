#!/bin/bash

while :; 
do
    locust --no-web -c 1 -r 1 -L INFO  &
    PROC=$1; sleep 0.7; kill $!
done
#locust --no-web -c 100 -r 100 -L INFO -r2
#locust --no-web -c 100 -r 100 -L INFO -r2

# EOF
