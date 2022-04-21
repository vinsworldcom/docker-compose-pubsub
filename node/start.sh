#/bin/sh

pkill python
pkill mosquitto
sleep 2
mosquitto -c mosquitto.conf -v 2>> /var/log/mosquitto-remote.log &
mosquitto -p 1884 -v 2>> /var/log/mosquitto-local.log &
python ./subproxy.py &
python ./app.py &
