#!/bin/bash
# Start the TzQuant BP server on port 8080 (customizable: ./start.sh 9000)
set -e
PORT="${1:-8080}"
python3 "$(dirname "$0")/serve.py" "$PORT"
