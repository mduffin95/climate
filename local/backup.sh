#!/bin/sh
rsync -avz --rsync-path="sudo rsync" --remove-source-files matt@raspberrypi.local:/var/log/climate_* ~/Dev/climate/local/logs/
