#!/bin/bash
if [ $# == 1 ]; then
  $1 -W ignore src/generate_tournaments.py
else
  echo "Usage: ./generate_tournaments.sh \"path to SageMath python interpreter\""
fi