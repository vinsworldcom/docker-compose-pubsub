#!/usr/bin/env python3

from datetime import datetime
import socket
import threading
import time

import paho.mqtt.client as mqtt

TOPIC = "shared_data"

local_ip = socket.gethostbyname(socket.gethostname())

p = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, local_ip) #create new instance
p.connect(local_ip)
# p.subscribe(TOPIC)
# p.on_message=on_message
p.loop_start()

def pub():
    """Publish function."""
    while True:
        p.publish(TOPIC, f"{local_ip} / {datetime.now()}")
        time.sleep(2)

def on_message(client, userdata, message):
    """MQTT on message callback."""
    print(str(message.payload.decode("utf-8")))

sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, local_ip) #create new instance
sub.connect("localhost", 1884)
sub.subscribe(TOPIC)
sub.on_message=on_message
sub.loop_start()

app = threading.Thread(target=pub, args=())
app.start()
