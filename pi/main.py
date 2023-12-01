import adafruit_ahtx0
import board
import json
import logging
import logging.config

logging.config.fileConfig('/home/matt/logging.conf')
# set up logger
logger = logging.getLogger('simpleExample')

# Setup I2C Sensor
sensor = adafruit_ahtx0.AHTx0(board.I2C())

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
  return '{:.2f}'.format(input)

temp = sensor.temperature
humidity = sensor.relative_humidity
logger.info("Reading taken", extra={ "temperature" : temp, "humidity" : humidity })
