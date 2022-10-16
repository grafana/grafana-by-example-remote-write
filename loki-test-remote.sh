#!/bin/bash
#
#
DURATION_SEC=${1:-"120"} # Assume seconds
INTERVAL_SEC=${2:-"15"} # Assume seconds
JOB_NAME=${3:-"rndwords2"}
HOSTNAME=$hostname


_findAltCmd() {
  RESULT=""
  CMD_ALT_LIST=$1
  for ALT_CMD in ${CMD_ALT_LIST[@]}; do
    CMD_A=$(which $ALT_CMD)
    if [ "$CMD_A" != "" ]; then
      RESULT=$CMD_A
      break
    fi
  done
  echo $RESULT
}

_durationToSeconds() {
  DURATION_SEC=$1
  DURATION_SEC_LAST_CHAR=${DURATION_SEC: -1}
  if [ "$DURATION_SEC_LAST_CHAR" == "s" ]; then
    RESULT=$(( ${DURATION_SEC%?} * 1 ))
  elif [ "$DURATION_SEC_LAST_CHAR" == "m" ]; then
    RESULT=$(( ${DURATION_SEC%?} * 60 ))
  elif [ "$DURATION_SEC_LAST_CHAR" == "h" ]; then
    RESULT=$(( ${DURATION_SEC%?} * 60 * 60 ))
  elif [ "$DURATION_SEC_LAST_CHAR" == "d" ]; then
    RESULT=$(( ${DURATION_SEC%?} * 60 * 60 * 24 ))
  elif [ "$DURATION_SEC_LAST_CHAR" == "w" ]; then
    RESULT=$(( ${DURATION_SEC%?} * 60 * 60 * 60 * 7 ))
  else
    RESULT=$DURATION_SEC
  fi
  echo $RESULT
}

_lokiPost() {
  #LOKI_URL=${GRAFANA_LOGS_WRITE_URL/\/\////$GRAFANA_LOGS_USERNAME:$GRAFANA_LOGS_API_KEY@}""
  LOKI_URL="https://$GRAFANA_LOGS_USERNAME:$GRAFANA_LOGS_API_KEY@$GRAFANA_LOGS_HOST/loki/api/v1/push"
  JOB_NAME="test1";
  RND_N=$(( $RANDOM % 10 ))
  NOW_NS=$( date +%s000000000 );
  echo curl -H "Content-Type: application/json"  \
    -X POST """$LOKI_URL""" \
    -d "{\"streams\": [ { \"stream\": { \"job\": \"$JOB_NAME\" }, \"values\": [ [ \"$NOW_NS\", \"msg=$RND_N \" ] ] } ] } "
}

CMD_UUIDGEN=$(_findAltCmd 'uuid uuidgen')
$CMD_UUIDGEN

DURATION_SEC=$(_durationToSeconds ${DURATION_SEC})
echo "Running for $DURATION_SEC seconds with internval $INTERVAL_SEC"


START_TIME=$(date +%s)
END_TIME=$(( START_TIME + DURATION_SEC ))
CNT_I=0

#LOKI_URL=${GRAFANA_LOGS_WRITE_URL/\/\////$GRAFANA_LOGS_USERNAME:$GRAFANA_LOGS_API_KEY@}""
LOKI_URL="https://$GRAFANA_LOGS_USERNAME:$GRAFANA_LOGS_API_KEY@$GRAFANA_LOGS_HOST/loki/api/v1/push"
echo "Grafana Logs URI [$LOKI_URL]s"


while (true); do
  CNT_I=$((CNT_I+1))
  TIME_NOW=$(date +%s)
  TIME_REMAINING=$((END_TIME - TIME_NOW))

  NOW_NS=$( date +%s000000000 )
  LOG_DATA="$(_randomSentence )"
  echo "[$LOG_DATA]"
  #LOG_DATA=$( $CMD_UUIDGEN )
  RND_N=$(( $RANDOM % 10 ))

  if [ "$RND_N" -gt "5" ]; then
  DATA="
  {
    \"streams\": [ {
        \"stream\": { \"job\": \"$JOB_NAME\" },
        \"values\": [
            [ \"$NOW_NS\", \"msg=$LOG_DATA rnd=$RND_N\" ]
        ] } ] } "
  else
    DATA="
    {
      \"streams\": [ {
          \"stream\": { \"job\": \"$JOB_NAME\" },
          \"values\": [
              [ \"$NOW_NS\", \"msg=$LOG_DATA rnd=NA \" ]
          ] } ] } "
  fi
  echo "Writing"
  curl -v -H "Content-Type: application/json"  \
    -X POST """$LOKI_URL""" \
    -d "$DATA"


  echo $CNT_I, $TIME_REMAINING ---"$DATA"---
  if [ "$TIME_NOW" -gt "$END_TIME" ]; then
        echo "Stopping "
        break;
      else
        sleep $INTERVAL_SEC
  fi

done
