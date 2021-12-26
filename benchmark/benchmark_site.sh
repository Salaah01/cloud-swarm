#!/usr/bin/bash
# Set environment variable
. ~/env

# Run benchmark
ab -n $NUM_REQUESTS -c $NUM_REQUESTS $BENCHMARK_URL >results.txt

# Extract data from results
summary=$(grep 'Total:' results.txt)
min=$(echo $summary | awk '{print $2}')
max=$(echo $summary | awk '{print $6}')
mean=$(echo $summary | awk '{print $3}')

complete_requests=$(grep 'Complete requests:' results.txt | awk '{print $3}')
failed_requests=$(grep 'Failed requests:' results.txt | awk '{print $3}')

# Write results to a json file
echo '{' >results.json
echo '  "min": '$min',' >>results.json
echo '  "max": '$max',' >>results.json
echo '  "mean": '$mean',' >>results.json
echo '  "complete_requests": '$complete_requests',' >>results.json
echo '  "failed_requests": '$failed_requests >>results.json
echo '}' >>results.json
