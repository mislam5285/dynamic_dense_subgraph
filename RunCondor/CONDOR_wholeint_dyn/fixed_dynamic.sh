#!/bin/bash
D=(studentsSmall enronSmall facebookSmall)
#D=(enronSmall )
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
        #for k in {1..50}
        do

                line="${d}.txt ${d}_${b}_${k} ${k} ${b} ${n}"            
                #echo -append \"arguments = $line\" condor_description
                condor_submit -append "arguments = ${line}" condor_description

        done   
   done   
done
