#!/usr/bin/env bash
set -e

export PYTHONPATH=src

pip install .

python -m skillcorner.app.main