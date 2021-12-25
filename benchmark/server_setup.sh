#!/usr/bin/bash

# Script to ssh into a server, and setup the server for benchmarking.
ssh -o "StrictHostKeyChecking no" ubuntu@$1 "sudo apt update; sudo apt upgrade -y; sudo apt update; sudo apt install apache2-utils -y"

# If ssh connection is refused, try again after a short delay.
if [ $? -ne 0 ]; then
  echo -e "\033[91mConnection refused. Retrying in 5 seconds...\033[0m"
  sleep 5
  ssh -o "StrictHostKeyChecking no" ubuntu@$1 "sudo apt update; sudo apt upgrade -y; sudo apt update; sudo apt install apache2-utils -y"
fi

# If ssh connection is refused, try again after a longer delay.
if [ $? -ne 0 ]; then
  echo -e "\033[91mConnection refused. Retrying in 10 seconds...\033[0m"
  sleep 10
  ssh -o "StrictHostKeyChecking no" ubuntu@$1 "sudo apt update; sudo apt upgrade -y; sudo apt update; sudo apt install apache2-utils -y"
fi
