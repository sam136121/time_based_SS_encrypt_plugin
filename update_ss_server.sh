#!/bin/bash
ssserver -c /etc/shadowsocks.json -d stop
#to run encrypt program
python /root/encrypt_by_time_server.py 
ssserver -c /etc/shadowsocks.json -d start