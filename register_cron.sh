#!/bin/bash

script_dir=`pwd`

cronline='*/5 8-21 * * *'

script="$script_dir/pvAlert.sh"

(crontab -l && echo "$cronline $script ##PVALERT_CRON") | crontab -