#!/bin/bash

# Define the paths to your FastAPI projects
declare -a paths=("dfa_service" "ocr_service" "sex_service" "window_service")

# Define the ports on which your FastAPI projects will run
declare -a ports=("8000" "8001" "8002" "8003")

# Define the log file
logfile="ai_service.log"

local_log_file="service.log"
# Loop over the arrays and start each FastAPI project on its own port
for i in "${!paths[@]}"; do
  echo "Starting ${paths[$i]} on port ${ports[$i]}" | tee -a "$logfile"
  
  # Navigate to the project directory
  cd "${paths[$i]}"
  
  # Activate the virtual environment
  source venv/bin/activate
  
  # Run the FastAPI application
  uvicorn --host 0.0.0.0 --port "${ports[$i]}" app.main:app >> "$local_log_file" 2>&1 &
  
  # Deactivate the virtual environment
  deactivate
  
  # Navigate back to the original directory
  cd -
done

# Wait for all background processes to finish
wait