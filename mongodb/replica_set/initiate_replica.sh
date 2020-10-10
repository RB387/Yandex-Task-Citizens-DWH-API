#!/bin/bash

# You can add here more nodes of replica set

all=0
dev=0
prod=0
while [[ $1 == -* ]]; do
    case "$1" in
      -a|--all) all=1; shift;;
      -d|--dev) dev=1; shift;;
      -p|--prod) prod=1; shift;;
    esac
done

if [ "$all" = 1 ] || [ "$prod" = 1 ]
then
  echo "Starting prod replica set initialize"
  until mongo --host mongo_node0 --port 27017 --eval "print(\"waited for connection\")"
  do
      sleep 2
  done
  echo "Connection finished"

  echo "Creating prod replica set"
  # Can connect only inside docker. Use only for prod
  mongo --host mongo_node0 --port 27017 <<EOF
rs.initiate({
  _id : 'rs0',
  members: [
    { _id : 0, host : "mongo_node0:27017" }
  ]
})
EOF
  echo "Prod replica set created"
fi

if [ "$all" = 1 ] || [ "$dev" = 1 ]
then
  echo "Starting test_mongo replica set initialize"
  until mongo --host dev_mongo --port 10017 --eval "print(\"waited for connection\")"
  do
      sleep 2
  done
  echo "Connection finished"

  echo "Creating dev replica set"
  # Can connect only outside docker. Use for local debug and tests
  mongo --host dev_mongo --port 10017 <<EOF
rs.initiate({
  _id : 'dev-rs0',
  members: [
    { _id : 0, host : "127.0.0.1:10017" }
  ]
})
EOF
  echo "Dev replica set created"
fi