#!/bin/bash

for lett1 in {a..z}
do
    for lett2 in {a..z}
    do
        for lett3 in {a..z}
        do
            echo $lett1$lett2$lett3@$lett1$lett2$lett3.com  >> emails.txt
        done
    done
done

#head -n200 emails.txt > emails.txt

# EOF
