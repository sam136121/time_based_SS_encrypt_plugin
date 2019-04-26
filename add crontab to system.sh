#!/bin/bash
ehco '0 0 * * * sh /root/update_ss_server.sh &' >> /var/spool/cron/crontabs/root