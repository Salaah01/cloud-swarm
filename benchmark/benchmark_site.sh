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

# Write results to a json file
echo '{"min":'$min',"max":'$max',"mean":'$mean'}' >results.json
