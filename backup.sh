#!/bin/sh
rsync -avz --remove-source-files matt@raspberrypi.local:~/logs/* ~/Dev/climate/logs/
