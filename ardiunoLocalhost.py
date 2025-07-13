import serial
import time
import json
import paho.mqtt.client as mqtt

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
BASE_TOPIC = 'arduino'

mqtt_client = mqtt.Client()

def connect_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)
        exit()

connect_mqtt()

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print("Failed to connect to Arduino:", e)
    exit()

buffer = ""
while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if not line:
            continue

        if line == "{":
            buffer = line + "\n"
        elif line == "---":
            try:
                data_json = json.loads(buffer)

                mqtt_client.publish(f"{BASE_TOPIC}/temperature", data_json["temperature"]["value"])
                mqtt_client.publish(f"{BASE_TOPIC}/smoke", data_json["smoke"]["value"])
                mqtt_client.publish(f"{BASE_TOPIC}/smoke_level", data_json["smoke"]["level"])
                mqtt_client.publish(f"{BASE_TOPIC}/distance", data_json["distance"]["value"])
                mqtt_client.publish(f"{BASE_TOPIC}/light", data_json["light"]["value"])
                mqtt_client.publish(f"{BASE_TOPIC}/timestamp", data_json["timestamp"])

                print("Published each sensor to its own topic.")
            except json.JSONDecodeError as e:
                print("JSON parse error:", e)
            except KeyError as e:
                print("Missing expected field:", e)

            buffer = ""
        else:
            buffer += line + "\n"

    except KeyboardInterrupt:
        print("Stopped by user.")
        break
    except Exception as e:
        print("Unexpected error:", e)

arduino.close()
mqtt_client.disconnect()