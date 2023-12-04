# Indoor climate monitoring
A simple system for monitoring temperature and humidity data from my flat. 

The basic steps are as follows:
- Use systemd to run a couple of python scripts every minute to collect indoor and outdoor temp/humidity data.
- Log the results to `/var/log/climate` which is set up with a `tmpfs` mount.
- On my mac, run a cron job to `rsync` the log files on a regular basis (currently every 5 minutes).
- Use the ELK stack to consume, parse and index the log files and display pretty graphs.

# On the Mac

Create a bash script for syncing with RPI.
```
#!/bin/sh
rsync -avz --remove-source-files matt@raspberrypi.local:~/logs/* ~/Dev/climate/logs/
```

Edit crontab using `crontab -e` and add the following line in order to run the script on an hourly basis:
```
0 * * * * cd ~/Dev/climate && ./backup.sh
```

We now need to pick up the synced log files and ingest them into elasticsearch. To do that we need logstash:

```
brew install logstash-full kibana-full elasticsearch-full
```

Using brew serivces to run the ELK stack:

```
brew services list
```

# On the Pi

[Pi pins](https://pi4j.com/1.2/pins/model-a-rev2.html)

[DHT20 datasheet](https://cdn-shop.adafruit.com/product-files/5183/5193_DHT20.pdf)

DHT20 Pins to RPI pins

1. 5v DC (Pi pin 2)
2. SDA0 (Pi pin 3)
3. GND (Pi pin 25, or any other ground pin)
4. SCL0 (Pi pin 5)


### Timers

To run the `main.py` script on a scheduled basis I've used a systemd timer and service. These can be found at `/etc/systemd/system`:

- climate.service
```
[Unit]
Description=Sends temp and humidity data to ELK stack
Wants=climate.timer

[Service]
Type=oneshot
ExecStart=/home/matt/climate.sh

[Install]
WantedBy=multi-user.target
```

- climate.timer
```
[Unit]
Description=Logs climate metrics
Requires=climate.service

[Timer]
Unit=climate.service
OnCalendar=*-*-* *:*:00

[Install]
WantedBy=timers.target
```

# Use `tmpfs` for `/var/log`

I set up tmpfs for /var/log. This creates an in-memory drive and should help to reduce the number of writes made to the SD card. Hopefully this will increase its lifespan.
```
tmpfs /var/log  tmpfs defaults,noatime,size=16m 0 0
```

Then run `sudo mount -a` to load the new mount. Running `df -h` should show the new mount in place.

Following the approach mentioned [here](https://unix.stackexchange.com/questions/554788/mount-a-tmpfs-folder-on-startup-volatile-with-a-created-subfolder) 
we create a directory within /var/log that is owned by a non-root user. This allows us to write logs without using sudo.