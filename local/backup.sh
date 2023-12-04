#!/bin/sh
rsync -avz --remove-source-files matt@raspberrypi.local:/var/log/climate/climate_* ~/Dev/climate/local/logs/
