import tailer
from datetime import datetime
import json
from elasticsearch import Elasticsearch


es = Elasticsearch('http://localhost:9200')

for line in tailer.follow(open('test-log.log')):
    print(line)
    myhash = json.loads(line)
    dt = datetime.strptime(myhash['@timestamp'], '%d/%b/%Y:%H:%M:%S +%f')
    myhash['@timestamp'] = ("%sT%s+00:00"%(dt.date(),dt.time()))
    print(myhash)
    res = es.index(index="test-index", doc_type="log", body=myhash)
    print(res['result'])
