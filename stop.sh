#!/bin/bash

# Define the ports on which your FastAPI projects are running
declare -a ports=("8000" "8001" "8002" "8003")

# Loop over the ports and stop the service running on each port
for port in "${ports[@]}"; do
  echo "Stopping service on port $port"
  
  # Find the process ID of the service running on the port
  pid=$(lsof -t -i:$port)
  
  # If a process ID was found, kill the process
  if [ -n "$pid" ]; then
    kill -9 $pid
    echo "Service on port $port stopped"
  else
    echo "No service running on port $port"
  fi
done