#!/bin/bash
#D=(tumblr students enron facebook twitter)
D=(mails)
#D=(enron tumblr_3months CAStudents_10000)
B=(1 3 7)
#B=(7)
K=(1 3 5 7 10)
#K=(3 7)
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
