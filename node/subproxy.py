#!/usr/bin/env python3

import os
import paho.mqtt.client as mqtt
import socket
import time
import threading

topic = "shared_data"

local_ip = socket.gethostbyname(socket.gethostname())
remote_ips = []
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
    if rc == 0:
        client.subscribe(topic)

def on_message(client, userdata, message):
    p.publish(topic, str(message.payload.decode("utf-8")))

p = mqtt.Client(f"{local_ip}-proxy") #create new instance
p.connect("localhost", 1884)
# p.subscribe(topic)

def sub(ip):
    r = mqtt.Client(local_ip)
    while True:
        try:
            r.connect(ip)
            break
        except ConnectionRefusedError:
            time.sleep(1)
    r.subscribe(topic)
    r.on_connect = on_connect
    r.on_message = on_message
    r.loop_start()

remote_pubsubs = []
for ip in remote_ips:
    x = threading.Thread(target=sub, args=([ip]))
    x.start()

p.loop_forever()
