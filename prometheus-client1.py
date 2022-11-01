from prometheus_client import start_http_server
from prometheus_client import Summary
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
import prometheus_client
import random
import time
import sys
from datetime import datetime, timedelta
import platform


#
#
#https://github.com/prometheus/client_python

# Disabling Default Collector metrics
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

hostName = platform.node()
startTime = int( time.time() )
metricPrefix = "python"
# Define the metrics and labels
labelKeys = ["hostname"]

metrics = {
    "counters" : {
        "samples":      Counter("{}_samples_generated".format(metricPrefix),
                         "Number of samples generated", labelKeys) }, 
    "gauges": {
        "uptime":       Gauge("{}_uptime".format(metricPrefix),
                         "Uptime in seconds", labelKeys),
        "remtime":      Gauge("{}_remtime".format(metricPrefix),
                         "Time remianing in seconds", labelKeys),
        "lastSample":   Gauge("{}_last_sample".format(metricPrefix),
                         "Last sample value", labelKeys) },
    "histograms": {
        "samples":      Histogram("{}_samples".format(metricPrefix),
                         "Histogram of samples", labelKeys) },
    "summaries": {
        "sampleTime":   Summary("{}_sample_time_seconds".format(metricPrefix),
                         "Time spent generating samples", labelKeys) }
} # metrics


def showMetrics():
    for metricType in metrics.keys():
        for metricName in metrics[ metricType ].keys():
            for m in metrics[metricType][metricName]._samples():
                print("{}.{}:{}".format(metricType,metricName,m))

# Decorate function with metric.
summariesSampleTime = metrics["summaries"]["sampleTime"].labels(hostName).time()
@summariesSampleTime
def generateSample():
    n = random.triangular(0.0, 12.0, 0.6)
    metrics["gauges"]["lastSample"].labels(hostName).set(n)
    metrics["histograms"]["samples"].labels(hostName).observe(n)
    metrics["counters"]["samples"].labels(hostName).inc()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "unknown command"
    if cmd == "test1":
        # Add the static label values
        for metricType in metrics.keys():
            for metricName in metrics[ metricType ].keys():
                metrics[metricType][metricName].labels(hostName)
        runTimeSec = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
        timeIntervalSec = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        debug = sys.argv[4].lower() == "debug" if len(sys.argv) > 4 else False
        print( "runTimeSec: {} intervalSec: {} debug: {}".format(runTimeSec, timeIntervalSec, debug))
        
        # Start the server to expose the metrics 
        start_http_server(8000)
        timeoutTime = datetime.now() + timedelta(seconds=runTimeSec)
        while datetime.now() < timeoutTime:
            generateSample()
            metrics["gauges"]["uptime"].labels(hostName).set( int( time.time() ) - startTime )
            metrics["gauges"]["remtime"].labels(hostName).set((timeoutTime - datetime.now()).total_seconds())
            if debug:
                showMetrics()
            time.sleep(timeIntervalSec)
        
    elif cmd == "test":
        print("test")
    else:
        print("Unknown Commands: [{}]\n".format(cmd))
        print( "Commands are:")
        print("  test1 <run time seconds> <interval seconds> [debug]")

    exit()