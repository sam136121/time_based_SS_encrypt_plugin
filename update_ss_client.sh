#!/bin/bash
PID=`ps -w | grep "ssserver -c /etc/shadowsocks.json -d start"|grep -v grep $1| awk '{print $1}'`
kill -9 $PID
sleep 2
ssserver -c /etc/shadowsocks.json -d start

