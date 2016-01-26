# telegraf-cassandra
Config for monitoring Cassandra using Telegraf's "Jolokia" plugin

## Overview:
I've wanted to get away from the "metrics-graphite.jar" method of getting metrics from Cassandra for a long time. While it is possible to do this with Collectd and the "JMX" plugin, it involves "hacking" the CollectD protocol a little bit to get the number of tags required to make useful graphs (particularly when you get down to the "Tables grouped by KeySpace" level).

## Aim:
* To have metrics delivered to a central InfluxDB cluster
* To have metrics fully tagged (enables powerful "GROUP BY" queries)
* To enforce SSL and authentication on the InfluxDB end (which means no collectd or tsdb plugins)

## The solution:
* Download the Jolokia-agent JAR file to /usr/share/java: ```sudo wget http://search.maven.org/remotecontent?filepath=org/jolokia/jolokia-jvm/1.3.2/jolokia-jvm-1.3.2-agent.jar -o /usr/share/java/jolokia-jvm-1.3.2-agent.jar```
* Configure Cassandra's startup script to include the Jolokia agent with the defaults file provided in ```etc/default/cassandra```, then re-start Cassandra. It should now be running Jolokia (listening on ```http://localhost:8778```)
* Install telegraf https://influxdata.com/downloads/
* Use the config file provided under ```etc/telegraf/telegraf.d/telegraf-jolokia-cassandra.conf``` - this will periodically collect the pre-defined metrics from Jolkia, and Telegraf will forward them to wherever you like
* Import the Grafana dashboard ```Cassandra-Performance.json``` (created against a datasource called "InfluxDB (Telegraf)")
* Profit!

## The problems remaining to be solved:
* You'll notice a section of commented-out wildcard metrics in the lower half of the Telegraf config file. While these DO work, they will cruft up the InfluxDB database (because they don't come back broken into tags). This will ruin your clean experience. It may require a modification to the Jolokia plugin, or an inspiring configuration alternative.
