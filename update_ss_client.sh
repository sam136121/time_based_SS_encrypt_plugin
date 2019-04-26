#!/bin/bash
PID=`ps -w | grep "ssserver -c /etc/shadowsocks.json -d start"|grep -v grep $1| awk '{print $1}'`
kill -9 $PID
sleep 2
python /root/encrypt_by_time_server.py
ssserver -c /etc/shadowsocks.json -d start

