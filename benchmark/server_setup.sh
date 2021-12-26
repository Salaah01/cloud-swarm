#!/usr/bin/bash

# Script to ssh into a server, and setup the server for benchmarking. Try
# this every 5 seconds until 30 seconds at which point it will exit.

wait_time=0
while [ $wait_time -lt 30 ]; do
  sleep 5
  wait_time=$((wait_time + 5))

  commands='sudo apt update;'
  commands+='sudo apt upgrade -y;'
  commands+='sudo apt update;'
  commands+='sudo apt install -y apache2;'

  ssh -o "StrictHostKeyChecking no" ubuntu@$1 "$commands"

  if [ $? -eq 0 ]; then
    break
  fi
  echo -e '\033[91mFailed to setup server, trying in 5 seconds...\033[0m'
done
