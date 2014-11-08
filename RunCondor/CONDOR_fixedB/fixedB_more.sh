#!/bin/bash
export LD_LIBRARY_PATH=$PWD/../scripts/
#D=(tumblr students enron facebook twitter)
D=(facebook)
B=(7)
K=(32 33 34 35)
n=1
#U=(grbi dy)
U=(grbi)
for d in "${D[@]}"
do
   for b in "${B[@]}"
   do
        for k in "${K[@]}"
        #for k in {1..50}
        do
            for u in "${U[@]}"
            do
                line="${d}.txt ${d}_${b}_${k}_${u} ${k} ${b} ${u}"            
                #echo -append \"arguments = $line\" condor_description
                condor_submit -append "arguments = ${line}" condor_description
            done
        done   
   done   
done
