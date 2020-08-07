#!/bin/bash

usage_str="Usage: ./compressibility.sh \"path to SageMath python interpreter\" \"graph in dig6 format\" \"upper bound of compressibility (optional, default=10)\""

if [ $# == 2 ]; then
  $1 -W ignore src/compressibility.py $2
elif [ $# == 3 ]; then
  $1 -W ignore src/compressibility.py $2 $3
else
  echo $usage_str
fi