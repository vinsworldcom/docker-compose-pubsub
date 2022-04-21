# Publish Subscribe

## Overview

This uses `docker-compose` to create a small network of containers:

```
    |--> pubsub-node-1 (MQTT)
    |
    |--> pubsub-node-2 (MQTT)
           .
           .
           .
    |--> pubsub-node-X (MQTT)
```

Each container runs a publish / subscribe application.  In order to avoid
a single point of failure central broker or dealing with some kind of broker
sync protocol, this demonstration uses a subscribe proxy in each container to
subscribe to all remote brokers and service the local application.

```
    subproxy.py
      |----|
                               |  subscribe to all remote nodes
     pub -> MQTT "remote"      | ------------->
            broker :1883       | <-\    \----->
         [  remote | recv'd  ] |    \    \---->
app.py   [ msgs pub| to local] |     \
                   v           |      \- all remote pubs are recv'd
     sub <- MQTT "local"       |
            broker :1884       |
```

With this unconventional setup, each local application publishes and 
subscribes to a local node broker so the broker is always "up", regardless 
of whether remote nodes are reachable.  The 'app.py' publishes to the 
localhost "remote" broker and subscribes to the localhost "local" broker.

The 'subproxy.py' application subscribes to all remote node "remote" brokers 
and any subscription traffic it receives is the published to the localhost 
"local" broker - for 'app.py' to receive.  The 'subproxy.py' handles 
reconnects and resubscriptions in the case of network failure.

## Build

To launch, just open a terminal, go to the same level with
'docker-compose.yml', and execute:

`docker-compose up -d --scale node=X`

Where 'X' is the number of pubsub nodes wanted - 3 is recommended at
least.

This will spin up the Docker architecture.

### Test

Login to each container:

`docker exec -it pubsub-node-X /bin/sh`

And run in each container:

`./start.sh`

You will see the time of day from each of the remote nodes begin printing. 
In one node, stop the demo by running in that container:

`./stop.sh`

Watch the other containers continue to receive updates from the remaining 
nodes.  Now restart the application in the container in which it was stopped:

`./start.sh`

See the time of day from all the remotes begin to be received again on all 
nodes.

Log files for 'mosquitto' brokers can be found at:

```
tail -f /var/log/mosquitto-local.log
tail -f /var/log/mosquitto-remote.log
```

### Cleanup

To quit (`CTRL+C` in the terminal if not called with `-d` option)

`docker-compose down`
