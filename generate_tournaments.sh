#!/bin/bash
if [ $# == 1 ]; then
  $1 -m pytest -W ignore src/tests
else
  echo "Usage: ./generate_tournaments.sh \"path to SageMath python interpreter\""
fi