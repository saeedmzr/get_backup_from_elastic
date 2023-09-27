#!/bin/bash
set -e

# Start Elasticsearch as a background service
elasticsearch &

# Sleep for a few seconds to allow Elasticsearch to start (adjust as needed)
sleep 30

# Run your script
python3 elastic_make_snapshots.py
