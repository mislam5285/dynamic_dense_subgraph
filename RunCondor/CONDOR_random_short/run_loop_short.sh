#!/bin/sh
export LD_LIBRARY_PATH=$PWD/../scripts/:$PWD
python ./../scripts/loop_and_short.py $1 $2 $3 $4 $5 $6
