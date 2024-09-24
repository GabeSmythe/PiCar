#!/bin/bash

# Creates the virtual environment and runs main.py for lab3. Required if any non-standard libraries included in main.py
# To run main.py and enter the virtual environment use source runMain.sh
# To run main without entering the venv use ./runMain.sh
# Create virtual environment with access to global packages (if not already created)
if [ ! -d "lab3" ]; then
  python3 -m venv --system-site-packages lab3
fi

# Activate virtual env
source lab3/bin/activate

# Install the required packages
pip install keyboard

# Run main.py using root user using venv's python interpreter
sudo $(which python3) main.py
