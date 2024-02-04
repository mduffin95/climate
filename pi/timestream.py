from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import board
import adafruit_ahtx0

# MQTT config (clientID must be unique within the AWS account)
clientID = "XXXX-XXXX-XXXXX-XXXXX"
endpoint = "XXXXXXXX.[AWS_REGION].amazonaws.com"  # Use the endpoint from the settings page in the IoT console
port = 8883
topic = "raspberry/temphumid"

# Init MQTT client
mqttc = AWSIoTMQTTClient(clientID)
mqttc.configureEndpoint(endpoint, port)
mqttc.configureCredentials(
    "certs/AmazonRootCA1.pem",
    "certs/raspberry-private.pem.key",
    "certs/raspberry-certificate.pem.crt",
)


# Send message to the iot topic
def send_data(message):
    mqttc.publish(topic, json.dumps(message), 0)
    print("Message Published")


# Loop until terminated
def loop():
    # Init the dht device with data pin connected
    # dhtDevice = adafruit_dht.DHT11(board.D17)
    dhtDevice = adafruit_ahtx0.AHTx0(board.I2C())

    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.relative_humidity
            print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))

            message = {"temperature": temperature, "humidity": humidity}

            # Send data to topic
            send_data(message)

            time.sleep(3)
        except (
            RuntimeError
        ) as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])


# Main
if __name__ == "__main__":
    print("Starting program...")
    try:
        # Connect
        mqttc.connect()
        print("Connect OK!")

        # Main loop called
        loop()
    except KeyboardInterrupt:
        mqttc.disconnect()
        exit()
