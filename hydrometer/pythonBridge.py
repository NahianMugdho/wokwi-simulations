# import subprocess
# import paho.mqtt.client as mqtt
# import threading
# import ssl
# import time
# import json
# import os

# # ---------- MQTT CONFIG ----------
# BROKER = "localhost"
# PORT = 8883
# USERNAME = "admin"
# PASSWORD = "StrongPassword123"
# CA_CERT = "broker.crt"

# ESP_TOPIC = "ESP/sensor"
# CONTROL_TOPIC = "control/led"   # topic for controlling LED

# # ---------- WOKWI CONFIG ----------
# script_dir = os.path.dirname(os.path.abspath(__file__))  # folder of this script
# WOKWI_CMD = ["wokwi-cli", script_dir]

# proc = None  # Global process handle

# # ---------- MQTT CLIENT ----------
# client = mqtt.Client(client_id="py_bridge", clean_session=True)
# client.username_pw_set(USERNAME, PASSWORD)
# client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_insecure_set(True)

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("[MQTT] ✅ Connected")
#         client.subscribe(CONTROL_TOPIC, qos=1)
#     else:
#         print(f"[MQTT] ❌ Failed, rc={rc}")

# def on_message(client, userdata, msg):
#     global proc
#     payload = msg.payload.decode().strip()
#     print(f"[MQTT] Received {msg.topic}: {payload}")

#     if proc and proc.stdin:
#         try:
#             proc.stdin.write(payload + "\n")
#             proc.stdin.flush()
#             print(f"[Wokwi] ← Sent command: {payload}")
#         except Exception as e:
#             print(f"[Wokwi] ❌ Write error: {e}")

# client.on_connect = on_connect
# client.on_message = on_message

# # ---------- WOKWI READER ----------
# def wokwi_reader():
#     global proc
#     try:
#         # Ensure Wokwi project is initialized
#         if not os.path.exists(os.path.join(script_dir, "wokwi.toml")) or not os.path.exists(os.path.join(script_dir, "diagram.json")):
#             print("[Wokwi] ⚠ wokwi.toml or diagram.json missing, initializing project...")
#             subprocess.run(["wokwi-cli", "init"], cwd=script_dir, check=True)

#         proc = subprocess.Popen(
#             ["wokwi-cli", "."],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             stdin=subprocess.PIPE,
#             text=True,
#             cwd=script_dir
#         )
#         print("[Wokwi] ▶ Simulation started...")
#         for line in proc.stdout:
#             line = line.strip()
#             if line:
#                 print(f"[Wokwi] → {line}")
#                 try:
#                     json.loads(line)
#                     client.publish(ESP_TOPIC, line, qos=1)
#                 except json.JSONDecodeError:
#                     client.publish(ESP_TOPIC, line, qos=1)
#     except Exception as e:
#         print(f"[Wokwi] ❌ Error: {e}")
#     finally:
#         if proc:
#             proc.terminate()
#             print("[Wokwi] ⏹ Simulation stopped.")

# # ---------- MAIN ----------
# if __name__ == "__main__":
#     client.connect(BROKER, PORT, keepalive=60)
#     client.loop_start()

#     t = threading.Thread(target=wokwi_reader, daemon=True)
#     t.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\n[Main] Shutting down...")
#     finally:
#         client.loop_stop()
#         client.disconnect()
#         if proc:
#             proc.terminate()
import paho.mqtt.client as mqtt
import threading
import ssl
import time
import json
import serial  # For connecting to forwarded serial

# ---------- MQTT CONFIG ----------
BROKER = "localhost"
PORT = 8883
USERNAME = "admin"
PASSWORD = "StrongPassword123"
CA_CERT = "broker.crt"

ESP_TOPIC = "ESP/sensor"
CONTROL_TOPIC = "control/led"   # topic for controlling LED

# ---------- SERIAL CONFIG ----------
SERIAL_URL = "rfc2217://localhost:9333"  # Matches [serial] port in wokwi.toml
ser = None  # Global serial handle

# ---------- MQTT CLIENT ----------
client = mqtt.Client(client_id="py_bridge", clean_session=True)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] ✅ Connected")
        client.subscribe(CONTROL_TOPIC, qos=1)
    else:
        print(f"[MQTT] ❌ Failed, rc={rc}")

def on_message(client, userdata, msg):
    global ser
    payload = msg.payload.decode().strip()
    print(f"[MQTT] Received {msg.topic}: {payload}")

    if ser and ser.is_open:
        try:
            ser.write((payload + "\n").encode())
            ser.flush()
            print(f"[Wokwi] ← Sent command: {payload}")
        except Exception as e:
            print(f"[Wokwi] ❌ Write error: {e}")

client.on_connect = on_connect
client.on_message = on_message

# ---------- WOKWI SERIAL READER ----------
def wokwi_reader():
    global ser
    try:
        ser = serial.serial_for_url(SERIAL_URL, baudrate=115200, timeout=1)
        print("[Wokwi] ▶ Connected to serial forward...")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"[Wokwi] → {line}")
                try:
                    json.loads(line)  # Validate as JSON
                    client.publish(ESP_TOPIC, line, qos=1)
                    print(f"[MQTT] Published to {ESP_TOPIC}: {line}")
                except json.JSONDecodeError:
                    pass  # Skip non-JSON lines (e.g., boot messages)
    except Exception as e:
        print(f"[Wokwi] ❌ Error: {e}")
    finally:
        if ser:
            ser.close()
            print("[Wokwi] ⏹ Serial connection stopped.")

# ---------- MAIN ----------
if __name__ == "__main__":
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    t = threading.Thread(target=wokwi_reader, daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
    finally:
        client.loop_stop()
        client.disconnect()
        if ser:
            ser.close()