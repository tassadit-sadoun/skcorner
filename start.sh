#!/usr/bin/env bash
set -e

export PYTHONPATH=src

python -m skillcorner.app.main  data.log
