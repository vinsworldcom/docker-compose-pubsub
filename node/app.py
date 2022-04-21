#!/usr/bin/env python3

from datetime import datetime
import paho.mqtt.client as mqtt
import socket
import threading
import time

topic = "shared_data"

local_ip = socket.gethostbyname(socket.gethostname())

p = mqtt.Client(local_ip) #create new instance
p.connect(local_ip)
# p.subscribe(topic)
# p.on_message=on_message
p.loop_start()

def pub():
    while True:
        p.publish(topic, f"{local_ip} / {datetime.now()}")
        time.sleep(2)

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

sub = mqtt.Client(local_ip) #create new instance
sub.connect("localhost", 1884)
sub.subscribe(topic)
sub.on_message=on_message
sub.loop_start()

app = threading.Thread(target=pub, args=())
app.start()
