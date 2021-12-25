#!/usr/bin/bash

# Script to setup the server for benchmarking. This involves writing an
# environment variables file and scp'ing it to the server as well as
host=$1
time=$2
num_requests=$3
benchmark_url=$4

host_user=ubuntu
benchmark_script_path="$(dirname $BASH_SOURCE[0])/benchmark_site.sh"

# Environment variables
env_vars="NUM_REQUESTS=${num_requests}\n"
env_vars+="BENCHMARK_URL=${benchmark_url}\n"

env_file=$(mktemp /tmp/env_vars.XXXXXX)
echo -e $env_vars >$env_file

scp $env_file $host_user@$host:~/env
scp $benchmark_script_path $host_user@$host:~/.

rm $env_file

ssh $host_user@$host "at -t $time -f benchmark_site.sh"
