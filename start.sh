#!/bin/bash
set -e

echo "Starting job..."

python -m skillcorner.app.main data.log
