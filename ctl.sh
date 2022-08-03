#!/bin/bash
#
#
CMD=${1:-"help"}

if [ $CMD == "configure" ]; then
  curl --create-dirs -L https://raw.githubusercontent.com/gogo/protobuf/master/gogoproto/gogo.proto -o gogoproto/gogo.proto
  curl --create-dirs -L -O https://raw.githubusercontent.com/prometheus/prometheus/main/prompb/remote.proto
  curl --create-dirs -L -O https://raw.githubusercontent.com/prometheus/prometheus/main/prompb/types.proto

elif [ $CMD == "install" ]; then
  brew install protobuf
  pip3 install --upgrade protobuf

elif [ $CMD == "build-pb" ]; then
  # Requires protobuf: brew install protobuf
  mkdir -p gogoproto
  protoc -I=. -I=./gogoproto --python_out=. gogoproto/gogo.proto
  protoc -I=. -I=./gogoproto --python_out=. types.proto
  protoc -I=. -I=./gogoproto --python_out=. remote.proto

elif  [ $CMD == "build-clean" ]; then
  rm -rf gogoproto
  rm -rf types.proto remote.proto
  rm -rf *_pb2.py

elif [ $CMD == "test" ]; then
  echo "test"

else
  echo "Commands: "
  echo "          configure"
  echo "          build-pd | build-clean "
fi

exit 0
