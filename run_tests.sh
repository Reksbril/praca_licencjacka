#!/bin/bash
if [ $# == 1 ]; then
  $1 -m pytest -W ignore src/tests
else
  echo "Usage: ./run_tests.sh \"path to SageMath python interpreter\""
fi
