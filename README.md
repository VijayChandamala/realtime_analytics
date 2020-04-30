# Realtime_analytics
### A real time analytics based on nginx logs

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
