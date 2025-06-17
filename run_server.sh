#!/bin/bash

# Activate virtual environment and run the MCP server
source venv/bin/activate
export PYTHONPATH="src:$PYTHONPATH"
cd src
python3 main.py