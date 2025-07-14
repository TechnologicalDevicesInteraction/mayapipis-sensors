import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import subprocess
import json
import paho.mqtt.client as mqtt
import psycopg2
from psycopg2 import pool

FAKE_SCRIPT = "python3 fake_data_emqx_publisher.py"
MQTT_BROKER   = ""
MQTT_PORT     = 
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
BASE_TOPIC    = ""

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
                conn = db_pool.getconn()
                try:
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO sensor_readings (timestamp, temperature, smoke, smoke_level, distance, light)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                data["timestamp"],
                                data["temperature"]["value"],
                                data["smoke"]["value"],
                                data["smoke"]["level"],
                                data["distance"]["value"],
                                data["light"]["value"]
                            )
                        )
                    conn.commit()
                    print("📥 Data inserted into PostgreSQL")
                finally:
                    db_pool.putconn(conn)

                client.publish(f"{BASE_TOPIC}/temperature", data["temperature"]["value"])
                client.publish(f"{BASE_TOPIC}/smoke", data["smoke"]["value"])
                client.publish(f"{BASE_TOPIC}/smoke_level", data["smoke"]["level"])
                client.publish(f"{BASE_TOPIC}/distance", data["distance"]["value"])
                client.publish(f"{BASE_TOPIC}/light", data["light"]["value"])
                client.publish(f"{BASE_TOPIC}/timestamp", data["timestamp"])
                print("📤 Block published to HiveMQ Cloud")
            except Exception as e:
                print("❗ Error processing JSON or database:", e)
            buffer = ""
        else:
            buffer += line + "\n"

except KeyboardInterrupt:
    print("🛑 Interrupted by user.")

finally:
    proc.terminate()
    client.loop_stop()
    client.disconnect()
    db_pool.closeall()
    print("🔌 Disconnected and closed.")
