#!/usr/bin/bash

# Fetches benchmark results from a server.
host=$1
user=ubuntu
base_dir=$(dirname $BASH_SOURCE[0])

mkdir -p "${base_dir}/results"

wait_time=0

while [ $wait_time -lt 90 ]; do
  sleep 5
  wait_time=$((wait_time + 5))

  scp $user@$host:results.json "${base_dir}/results/${host}.json"
  if [ $? -eq 0 ]; then
    break
  fi

  echo -e '\033[91mFailed to fetch results from server, trying in 5 seconds...\033[0m'
done
