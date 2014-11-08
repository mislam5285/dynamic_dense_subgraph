#!/bin/bash
#if [ -f $PWD/../set_env.sh ]; then
#    source $PWD/../set_env.sh
#fi

set -x
export LD_LIBRARY_PATH=$PWD/../scripts/

D=(studentsSmall facebookSmall enronSmall)
#D=(enron tumblr_3months CAStudents_10000)
B=(1 3)
K=(1 3)
n=1
#U=(grbi dy)

for d in "${D[@]}"
do
   for b in "${B[@]}"
   do
        for k in "${K[@]}"
        do

            line="${d}.txt ${d}_${b}_${k} ${k} ${b} ${n}"            
            #echo -append \"arguments = $line\" condor_description
            condor_submit -append "arguments = ${line}" condor_description

        done   
   done   

done
