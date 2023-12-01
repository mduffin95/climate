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

# On the Pi

[Pi pins](https://pi4j.com/1.2/pins/model-a-rev2.html)

[DHT20 datasheet](https://cdn-shop.adafruit.com/product-files/5183/5193_DHT20.pdf)

DHT20 Pins to RPI pins

1. 5v DC (Pi pin 2)
2. SDA0 (Pi pin 3)
3. GND (Pi pin 25, or any other ground pin)
4. SCL0 (Pi pin 5)


