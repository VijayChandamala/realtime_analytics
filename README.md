# Realtime_analytics
### A real time analytics based on nginx logs

Instead of setting up nginx with a site, we're going to generate dummy nginx logs using a shell script.

The Python-Log-pusher updates the timestamp to match the timestamp pattern compatible with ES timestamp pattern, converts the log into json and pushes it to ElasticSearch( usually a search engine, but here we're going to use it as TSDB).

Thinking why ES instead of a TSDB ?
Well the querying from Grafana is pretty much faster compared any other TSDB i've used so far, eg Prometheus.

Moving on.....,

Well that was the backend part where you do all the coding stuff.

Now it's time to visualize and see some colors.

We're gonna use an open source visualisation tool to create graphs, charts, and other types of analysis of the logs we're storing in our ES(elasticsearch).

Well, i'm not gonna spoon feed about how to use a simple graph tool. I'm guessing you can figure it out on your except installing and running it successfully using Docker.

### Step-by-step Set-Up

First off, we're going to make sure ES is installed and available for our python script to push logs to.

We can use a docker image of ElasticSearch instead of manual installation, because it's easy.

```docker run -itd --name elasticsearch -p 9200:9200 elasticsearch:6.5.0
#set enough vm memory to avoid es running out of memory

sudo sysctl -w vm.max_map_count=244655
```

Second, run grafana

```docker run -itd --name grafana -p 3000:3000 grafana/grafana```

Now, we have both ES and Grafana up and running. So we're going to start both the scripts one by one to start pushing data to ES.

First the shell-script

```./log-gen.sh```

This will start writing dummy logs to your test-log.log. you can verify if the script's working by printing the test-log file.

Next, log-parse.py

```python log-parse.py```

I've written some print statements to verify it's running properly.

Now, goto grafana, http://localhost:3000
login with username: admin, password: admin, configure the datasource, create graphs and charts based on your requirement.

### Ta Da! you have yourself a real-time analytics engine. (too silly to call this an analytics engine :P )



# Python-Log-pusher

```
import tailer
from datetime import datetime
import json
#dt=datetime.strptime(da, '%d/%b/%Y:%H:%M:%S +%f')
#print("%sT%s+00:00"%(dt.date(),dt.time()))

from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')

for line in tailer.follow(open('test-log.log')):
    print(line)
    myhash = json.loads(line)
    dt = datetime.strptime(myhash['@timestamp'], '%d/%b/%Y:%H:%M:%S +%f')
    myhash['@timestamp'] = ("%sT%s+00:00"%(dt.date(),dt.time()))
    res = es.index(index="test-index", doc_type="log", body=myhash)
    print(res['result'])
    
```

# Dummy-Nginx-Log-Generator

```

#!/bin/bash
while true
do
        a=$(date | awk '{print $3"/"$2"/"$6":"$4" +0000"}')
        array[0]='{"@timestamp": "'$a'", "user": "human", "status": "200", "host": "www.my-site.net", "method": "GET", "device": "mobile", "request_uri": "/products/1062234"}'
        array[1]='{"@timestamp": "'$a'", "user": "human", "status": "200", "host": "www.my-site.net", "method": "GET", "device": "tablet", "request_uri": "/products/1026214"}'
        array[2]='{"@timestamp": "'$a'", "user": "google-bot", "status": "200", "host": "www.my-site.net", "method": "GET", "device": "pc", "request_uri": "/products/3544234"}'
        array[3]='{"@timestamp": "'$a'", "user": "human", "status": "200", "host": "www.my-site.net", "method": "GET", "device": "mobile", "request_uri": "/products/3566634"}'
        array[4]='{"@timestamp": "'$a'", "user": "human", "status": "200", "host": "www.my-site.net", "method": "GET", "device": "mobile", "request_uri": "/products/3500034"}'
        size=${#array[@]}
        index=$(($RANDOM % $size))
        echo ${array[$index]} >> test-log.log
        sleep 1
done

```
