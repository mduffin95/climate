#!/bin/sh
rsync -avz --remove-source-files matt@raspberrypi.local:/var/log/climate.log ~/Dev/climate/local/logs/
