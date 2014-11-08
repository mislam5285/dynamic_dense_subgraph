#!/bin/bash
export LD_LIBRARY_PATH=$PWD/../scripts/
D=(mails)
#D=(twitter facebook tumblr students enron)
#B=(3 7 10)
B=(3)
K=(1)
n=1
#U=(grbi dy)    
U=(grbi)
for d in "${D[@]}"
do
   for b in "${B[@]}"
   do
        for k in "${K[@]}"
        do
            for u in "${U[@]}"
            do
                line="${d}.txt ${d}_${b}_${k}_${u} ${k} ${b} ${n} ${u}"            
                #echo -append \"arguments = $line\" condor_description
                condor_submit -append "arguments = ${line}" condor_description
            done
        done   
   done   
done
