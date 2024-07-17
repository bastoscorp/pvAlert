#!/bin/bash

(crontab -l | grep -v "##PVALERT_CRON") | crontab -
