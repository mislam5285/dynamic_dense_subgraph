#!/bin/bash
export LD_LIBRARY_PATH=$PWD/../scripts/

#D=(tumblr enron twitter facebook students)
D=(facebook)
#B=(0.050 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1)
B=(1)
K=(7)
n=1
#U=(grbi dy)
U=(grbi)
for d in "${D[@]}"
do
   for b in "${B[@]}"
   #for b in {1..30}
   do
        for k in "${K[@]}"        
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
