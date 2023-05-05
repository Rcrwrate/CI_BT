#!/bin/bash
list=`wget -qO- https://trackerslist.com/all.txt|awk NF|sed ":a;N;s/\n/,/g;ta"`
if [ -z "`grep "bt-tracker" aria2.conf`" ]; then
    sed -i '$a bt-tracker='${list} aria2.conf
    echo add......
else
    sed -i "s@bt-tracker=.*@bt-tracker=$list@g" aria2.conf
    echo update......
fi