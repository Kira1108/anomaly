#!/bin/bash

# Define the paths to your FastAPI projects
declare -a paths=("dfa_service" "ocr_service" "sex_service" "window_service")

# Loop over the arrays and create a virtual environment and install dependencies for each FastAPI project
for i in "${paths[@]}"; do
  echo "Setting up ${i}"
  
  # Navigate to the project directory
  cd "$i"
  
  # Create a virtual environment
  python3 -m venv venv
  
  # Activate the virtual environment
  source venv/bin/activate
  
  # Install dependencies
  pip install -r requirements-mac.txt
  
  # Deactivate the virtual environment
  deactivate
  
  # Navigate back to the original directory
  cd -
done