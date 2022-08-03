# grafana-by-example-remote-write
Examples of remote writing telemetry data to Grafana Metics, Logs and Traces

Build and run this example using:

## Remote write to Grafana Cloud Metrics endpoint
Example Python script to demonstrate remote write to a Grafana Cloud Metrics endpoint

Uses protocol buffer messages defined from Prometheus [prompb](https://github.com/prometheus/prometheus/tree/main/prompb) and [gogoprotobuf](https://github.com/gogo/protobuf/tree/master/gogoproto)

### Required environment variables

File: envvars-grafana-cloud.sh

```
export GRAFANA_METRICS_URL="https://prometheus-blocks-prod-us-central1.grafana.net/api/prom/push"
export GRAFANA_METRICS_USERNAME="[REQUIRED]"
export GRAFANA_METRICS_API_KEY="[REQUIRED]"
```

### Required environment

- Python3
- Google Protocol Buffer [compiler](https://developers.google.com/protocol-buffers)
- pip3 install python-snappy
- pip3 install requests

### Example usage

Install the Protocol Buffer compiler, protoc using:
```
# On macOS:
brew install protobuf
```

```
# Download the gogo.proto, remote.proto and types.proto
./ctl.sh configure

# Install MacOs protobuf and Python protobuf
./ctl.sh install

# Build the Python protobuf libraries
./ctl.sh build-pb

# Source the environment variables for the Grafana Cloud Prometheus endpoint
source envvars-grafana-cloud.sh

# Run the example
python3 python3 metrics-generator.py single 5 100

```
Validate the metrics have be received at the Grafana Cloud Prometheus instance under the labels:
```
job="test1"
test1_http_errors_total{}
test1_http_requests_total{}
```

## Reference Documents

- Google Protocol Buffer [Guide](https://developers.google.com/protocol-buffers)
- Protocol Buffer Basics: Python [Guide](https://developers.google.com/protocol-buffers/docs/pythontutorial)
- Protobuf definitions for the OpenTelemetry protocol (OTLP) [metrics.proto](https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/metrics/v1/metrics.proto)
- OpenTelemetry Prometheus Remote Write Exporter [Python Package](https://pypi.org/project/opentelemetry-exporter-prometheus-remote-write/)
- Prometheus Potocol Buffer [prompb](https://github.com/prometheus/prometheus/tree/main/prompb)
- Promethues Metrics [Grafana Cloud](https://grafana.com/docs/grafana-cloud/metrics-prometheus/)
