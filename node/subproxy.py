#!/usr/bin/env python3

import os
import socket
import time
import threading

import paho.mqtt.client as mqtt

TOPIC = "shared_data"

local_ip  : str       = socket.gethostbyname(socket.gethostname())
remote_ips: list[str] = []
for i in range(1, 255):
    try:
        remote_ip = socket.gethostbyname(f"{os.environ['COMPOSE_PROJECT_NAME']}-node-{i}")
        if local_ip != remote_ip:
            remote_ips.append(remote_ip)
    except socket.gaierror:
        break

print(f"Local   = {local_ip}")
print(f"Remotes = {remote_ips}")

def on_connect(client, userdata, flags, rc):
    """MQTT on connect callback."""
    if rc == 0:
        client.subscribe(TOPIC)

def on_message(client, userdata, message):
    """MQTT on message callback."""
    p.publish(TOPIC, str(message.payload.decode("utf-8")))

p = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, f"{local_ip}-proxy") #create new instance
p.connect("localhost", 1884)
# p.subscribe(TOPIC)

def sub(remote_addr: str):
    """
    Subscribe function.

    Args:
        remote_addr (str): Remote IP address
    """
    r = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, local_ip)
    while True:
        try:
            r.connect(remote_addr)
            break
        except ConnectionRefusedError:
            time.sleep(1)
    r.subscribe(TOPIC)
    r.on_connect = on_connect
    r.on_message = on_message
    r.loop_start()

remote_pubsubs = []
for ip in remote_ips:
    x = threading.Thread(target=sub, args=(ip,))
    x.start()

p.loop_forever()
