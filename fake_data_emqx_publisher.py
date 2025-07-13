import time
import json
import random

def generate_fake_data():
    return {
        "timestamp": int(time.time() * 1000),
        "temperature": {"value": round(random.uniform(15.0, 40.0), 2), "unit": "C"},
        "smoke": {
            "value": random.randint(0, 800),
            "level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "unit": "raw"
        },
        "distance": {"value": round(random.uniform(2.0, 100.0), 2), "unit": "cm"},
        "light": {"value": random.randint(0, 1023), "unit": "raw"}
    }

if __name__ == "__main__":
    try:
        while True:
            data = generate_fake_data()
            print("{")
            print(f'  "timestamp": {data["timestamp"]},')
            print(f'  "temperature": {{"value": {data["temperature"]["value"]}, "unit": "{data["temperature"]["unit"]}"}},')
            print(f'  "smoke": {{"value": {data["smoke"]["value"]}, "level": "{data["smoke"]["level"]}", "unit": "{data["smoke"]["unit"]}"}},')
            print(f'  "distance": {{"value": {data["distance"]["value"]}, "unit": "{data["distance"]["unit"]}"}},')
            print(f'  "light": {{"value": {data["light"]["value"]}, "unit": "{data["light"]["unit"]}"}}')
            print("}")
            print("---")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped fake data publisher.")
