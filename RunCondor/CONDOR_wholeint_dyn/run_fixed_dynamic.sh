#!/bin/sh
export LD_LIBRARY_PATH=$PWD
python ./../scripts/fixed_dynamic.py $1 $2 $3 $4 $5
