from datetime import datetime
import calendar
import os
import requests
import snappy
import random
import sys
from datetime import datetime, timedelta
from time import strftime
import time
import json

def readJsonFile(fileName):
    j = {}
    try:
        j = json.load(open(fileName, "rb"))
    except Exception as e:
        sys.stderr.write("readJsonFile: failed: file: {} {}\n".format(fileName, e))
    return j

from remote_pb2 import (
    WriteRequest
)

from types_pb2 import (
    TimeSeries,
    Labels,
    Sample
)

# Grafana Cloud Prometheus Configuration
requiredEnvvars = [ "GRAFANA_METRICS_WRITE_URL", "GRAFANA_METRICS_USERNAME", "GRAFANA_METRICS_API_KEY" ]
config = {}
config["envvars"] = { v: os.environ[ v ] for v in requiredEnvvars }

def dt2ts(dt):
    """Converts a datetime object to UTC timestamp
    naive datetime will be considered UTC.
    """
    return calendar.timegm(dt.utctimetuple())

def addLabel(timeSeries, name, value):
    label = timeSeries.labels.add()
    label.name = name
    label.value = value

def addSample(timeSeries, value, nowdt=datetime.now() ):
    sample = timeSeries.samples.add()
    sample.value = value
    sample.timestamp = dt2ts(nowdt) * 1000

def remoteWrite(writeRequest):
    # Generate remoteWriteURL with user and key
    remoteWriteURL = "https://{user}:{key}@{url}".format(user=config["envvars"]["GRAFANA_METRICS_USERNAME"],
                                              key=config["envvars"]["GRAFANA_METRICS_API_KEY"],
                                              url=config["envvars"]["GRAFANA_METRICS_WRITE_URL"][8:])
    # Headers
    headers = {
        "User-Agent": "PythonRemoteWriteExample1",
        "Content-Encoding": "snappy",
        "Content-Type": "application/x-protobuf",
        "X-Prometheus-Remote-Write-Version": "0.1.0",
    }

    # auth=(config["envvars"]["GRAFANA_METRICS_USERNAME"],config["envvars"]["GRAFANA_METRICS_API_KEY"])

    # Remote Write
    try:
        #print("URL: {}, Value: [{}]".format(remoteWriteURL, writeRequest))
        data=snappy.compress(writeRequest.SerializeToString())
        r = requests.post(remoteWriteURL, headers=headers, data=data)
        print("Response: {} Bytes Sent {}".format(r, len(data)))
        print(r.text)
    except Exception as e:
        print("Error {} {}".format(e,r))

cmd = sys.argv[1] if len(sys.argv) > 1 else "unknown command"
if cmd == "single":
    delayWrSec = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    print("delayWrSec: {} samples: {}".format(delayWrSec, samples))
    for s in range(0, samples):
        # Generate the metric and remote write
        nowdt = datetime.utcnow()
        nowMs = dt2ts(nowdt) * 1000
        wr = WriteRequest()
        ts1 = wr.timeseries.add()
        addLabel(ts1, "__name__", "test1_http_requests_total")
        addLabel(ts1, "job", "test1")
        addLabel(ts1, "host", "host1")
        addSample(timeSeries=ts1, value=random.randrange(0,100), nowdt=nowdt)
        ts2 = wr.timeseries.add()
        addLabel(ts2, "__name__", "test1_http_errors_total")
        addLabel(ts2, "job", "test1")
        addLabel(ts2, "host", "host1")
        addSample(timeSeries=ts2, value=random.randrange(0,100), nowdt=nowdt)  
        remoteWrite(wr)
        print("{} now {} delay {} ts {}, tsMs {}".format(s, datetime.utcnow(), delayWrSec, nowdt, nowMs))
        if delayWrSec > 0:
            time.sleep(delayWrSec)


else:
    sys.stderr.write("Unknown Commands: [{}]\n".format(cmd))
