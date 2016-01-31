#!/usr/bin/env python
import argparse
import json
import urllib

# Command-line arguments:
parser = argparse.ArgumentParser(
	description = 'Process some integers.'
)
parser.add_argument(
	'--host',
	dest = 'jolokia_host',
	default = 'localhost',
	help = 'Jolokia host (default = "localhost")'
)
parser.add_argument(
	'--port',
	dest = 'jolokia_port',
	default = '8080',
	help = 'Jolokia port (default = "8080")'
)
parser.add_argument(
	'--metric',
	dest = 'metric_name',
	default = 'ReadLatency',
	help = 'Metric to get [default="ReadLatency", "CoordinatorReadLatency", "WriteLatency", "ReadTotalLatency", "WriteTotalLatency", "LiveDiskSpaceUsed"]'
)
args = parser.parse_args()


# Put together a Jolokia URL:
jolokia_url = "http://%s:%s/jolokia/read/org.apache.cassandra.metrics:type=ColumnFamily,keyspace=*,scope=*,name=%s" % (args.jolokia_host, args.jolokia_port, args.metric_name)

# Get JSON data from Jolokia:
response = urllib.urlopen(jolokia_url)

# Load the data into a dictionary:
jolokia_data = json.loads(response.read())

# Go through the results (one per column_family):
for column_family_path in jolokia_data['value']:

	# Break up the column_family_path to derive tags:
	tags = {}
	for tag in column_family_path.split(':')[1].split(','):
		tag_key = tag.split('=')[0]
		tag_value = tag.split('=')[1]
		tags[tag_key] = tag_value

	# Now derive the values:
	field_values = []
	for field in jolokia_data['value'][column_family_path]:
		field_values.append("%s=%s" % (field, jolokia_data['value'][column_family_path][field]))

	# Now print the metric out in Influx format ("cpu,cpu=cpu0,host=foo,datacenter=us-east usage_idle=99,usage_busy=1"):
	print("cassandra_columnfamily_%s,keyspace=%s,column_family=%s %s" % (args.metric_name, tags['keyspace'], tags['scope'], ','.join(field_values)))
