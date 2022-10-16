import os
import sys
import time
from datetime import datetime
from datetime import datetime, timedelta
import requests
import json
import random


lokiWriteURL = "{0}://{1}:{2}@{3}:{4}".format("http",
                                              os.environ["GRAFANA_LOGS_USERNAME"],
                                              os.environ["GRAFANA_LOGS_API_KEY"],
                                              os.environ["GRAFANA_LOGS_HOST"],
                                              "/loki/api/v1/push")


def writeLoki(jobName, logMessageStr):
    nowNs = int(time.time() * 1000000000)
    stream = {
        "stream": {"job": jobName},
        "values": [
            [str(nowNs), logMessageStr]
        ]
    }
    lokiData = {"streams": [stream]}
    headers = {"Content-Type": "application/json"}
    data = json.JSONEncoder().encode(lokiData)
    s = requests.session()
    r = s.post(lokiWriteURL, headers=headers, data=data)
    print(data)
    print(r.text)
    print(r.status_code)


def postLokiData(logMessageStr):
    headers = {"Content-Type": "application/json"}
    data = json.JSONEncoder().encode(lokiData)
    s = requests.session()
    r = s.post(lokiWriteURL, headers=headers, data=data)
    # print(data)
    # print(r.text)
    print(r.status_code)


cmd = sys.argv[1] if len(sys.argv) > 1 else "unknown command"
if cmd == "test1":
    logJson = {"val1": random.randrange(
        1, 10), "val2": random.randrange(1, 10), }
    writeLoki("test1", json.dumps(logJson))

elif cmd == "test2":
    logMessageStr = "val1={} val2={}".format(
        random.randrange(1, 10), random.randrange(1, 10))
    writeLoki("test2", logMessageStr)

elif cmd == "streams":
    durationMinutes = int(sys.argv[2])if len(sys.argv) > 2 else 1
    ratePerMinute = int(sys.argv[3])if len(sys.argv) > 3 else 1
    nStreams = int(sys.argv[4])if len(sys.argv) > 4 else 1
    delaySec = 60.0 / ratePerMinute
    timeoutSec = durationMinutes * 60
    timeoutTime = datetime.now() + timedelta(seconds=timeoutSec)
    reportTime = datetime.now() + timedelta(seconds=60)
    startTime = datetime.now()
    hostNames = ["host1", "host2", "host3", "host4"]
    serviceNames = ["config", "input", "output", "writer"]
    logLevels = ["info", "error", "warning", "debug"]
    while datetime.now() < timeoutTime:
        nowNs = int(time.time() * 1000000000)
        jobName = "streams"
        streamId = 1
        lokiData = {"streams": []}  # no streams
        for streamId in range(nStreams):
            logMessage = {"host":       random.choices(hostNames)[0],
                          "service":    random.choices(serviceNames)[0],
                          "level":      random.choices(logLevels)[0],
                          "value1":     streamId,  # random.randint(1,100),
                          "value2":     random.randint(1, 100)}
            #logMessageStr = "{msg}".format(msg=json.dumps(logMessage))
            streamData = {"stream": {"job": jobName, "id": streamId},
                          "values": [[str(nowNs), json.dumps(logMessage)]]}
            lokiData["streams"].append(streamData)
        print(json.dumps(lokiData))
        #postLokiData( json.dumps( lokiData )  )
        postLokiData(lokiData)
        if delaySec > 0:
            time.sleep(delaySec)

elif cmd == "text1file":
    durationMinutes = int(sys.argv[2])if len(sys.argv) > 2 else 1
    ratePerMinute = int(sys.argv[3])if len(sys.argv) > 3 else 1
    delaySec = 60.0 / ratePerMinute
    timeoutSec = durationMinutes * 60
    timeoutTime = datetime.now() + timedelta(seconds=timeoutSec)
    reportTime = datetime.now() + timedelta(seconds=60)
    startTime = datetime.now()
    hostNames = ["host1", "host2", "host3", "host4"]
    serviceNames = ["config", "input", "output", "writer"]
    logLevels = ["info", "error", "warning", "debug"]
    #print( "rate: delaySec: {}".format(delaySec))
    f1 = open("log1.txt", "a")
    while datetime.now() < timeoutTime:
        logMessageStr = "{tsNs} {hostName} {serviceName} {value1} [{logLevel}] {value2}".format(
                        tsNs=time.time_ns(),
                        hostName=random.choices(hostNames)[0],
                        serviceName=random.choices(serviceNames)[0],
                        value1=random.randrange(1, 100),
                        logLevel=random.choices(logLevels)[0],
                        value2=random.randrange(1, 100))
        print(logMessageStr)
        f1.write(logMessageStr + "\n")
        f1.flush()
        if delaySec > 0:
            time.sleep(delaySec)  # writeLoki("text1", logMessageStr)
    f1.close()

else:
    print("Command unknown: {}".format(cmd))


exit()
