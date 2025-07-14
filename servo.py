import serial
import time
import paho.mqtt.client as mqtt

SERIAL_PORT = ''
BAUD_RATE = 9600

MQTT_BROKER   = ""
MQTT_PORT     = 
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
MQTT_TOPIC    = ""

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

try:
    print("Reading from Arduino and publishing to MQTT...")
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    temperature = float(line)
                    payload = {"temperature_c": temperature}
                    client.publish(MQTT_TOPIC, str(payload))
                    print(f"Published: {payload}")
                except ValueError:
                    print("Received non-numeric data:", line)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    ser.close()
    client.loop_stop()
    client.disconnect()
