import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import random
from paho.mqtt import client as mqtt_client

# Set the sensor type and the GPIO pin for DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Replace with the GPIO pin number you are using for DHT11

# Set the GPIO pins for the ultrasonic sensor
GPIO_TRIG = 11  # Replace with the GPIO pin number you are using for TRIG
GPIO_ECHO = 18  # Replace with the GPIO pin number you are using for ECHO

# Set the GPIO pin for the gas sensor
DO_PIN = 7  # Replace with the actual GPIO pin number you are using for the gas sensor

# MQTT broker configuration
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'publish-{random.randint(0, 1000)}'

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(DO_PIN, GPIO.IN)
GPIO.setwarnings(False)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def read_sensors():
    # Read the humidity and temperature from DHT11
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is None or temperature is None:
        humidity, temperature = 0.0,0.0

    # Measure distance using the ultrasonic sensor
    GPIO.output(GPIO_TRIG, GPIO.LOW)
    time.sleep(2)  # Wait for 2 seconds

    GPIO.output(GPIO_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        bounce_back_time = time.time()

    pulse_duration = bounce_back_time - start_time
    distance = round(pulse_duration * 17150, 2)

    # Read the state of the DO pin for the gas sensor
    gas_present = GPIO.input(DO_PIN)
    gas_state = "Gas Present" if gas_present == GPIO.LOW else "No Gas"

    return temperature, humidity, distance, gas_state

def publish(client):
    while True:
        temperature, humidity, distance, gas_state = read_sensors()
        if temperature is not None and humidity is not None:
            msg = f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%, Distance: {distance}cm, Gas State: {gas_state}"
        else:
            msg = f"Distance: {distance}cm, Gas State: {gas_state}, Temp/Humidity: Failed to retrieve"

        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send {msg} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(5)  # Wait for 5 seconds before the next reading

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()

if _name_ == '_main_':
    try:
        run()
    except KeyboardInterrupt:
        print("Monitoring stopped by user")
    finally:
        GPIO.cleanup()
        print("Exiting program")