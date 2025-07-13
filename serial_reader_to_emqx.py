import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import subprocess
import json
import paho.mqtt.client as mqtt

FAKE_SCRIPT = "python3 fake_data_emqx_publisher.py"

MQTT_BROKER   = "iotproject-ee93447b.a02.usw2.aws.hivemq.cloud"
MQTT_PORT     = 8883
MQTT_USERNAME = "Admin"
MQTT_PASSWORD = "Admin123"
BASE_TOPIC    = "arduino"

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

proc = subprocess.Popen(
    FAKE_SCRIPT.split(),
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True,
    bufsize=1
)

buffer = ""
try:
    for line in proc.stdout:
        line = line.strip()
        if line == "{":
            buffer = line + "\n"
        elif line == "---":
            try:
                data = json.loads(buffer)
                client.publish(f"{BASE_TOPIC}/temperature",  data["temperature"]["value"])
                client.publish(f"{BASE_TOPIC}/smoke",        data["smoke"]["value"])
                client.publish(f"{BASE_TOPIC}/smoke_level",  data["smoke"]["level"])
                client.publish(f"{BASE_TOPIC}/distance",     data["distance"]["value"])
                client.publish(f"{BASE_TOPIC}/light",        data["light"]["value"])
                client.publish(f"{BASE_TOPIC}/timestamp",    data["timestamp"])
                print("📤 Bloque publicado en HiveMQ Cloud")
            except Exception as e:
                print("❗ Error procesando JSON:", e)
            buffer = ""
        else:
            buffer += line + "\n"

except KeyboardInterrupt:
    print("🛑 Interrumpido por el usuario.")

finally:
    proc.terminate()
    client.loop_stop()
    client.disconnect()
    print("🔌 Desconectado y cerrado.")