#!/bin/bash
# SHRTY — run script
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "SHRTY: creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 shrty.py
