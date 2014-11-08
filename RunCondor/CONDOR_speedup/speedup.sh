#!/bin/bash
#D=(tumblr students enron facebook twitter)
#D=(facebookBig twitterBig facebook twitter)
D=(twitterBig facebookBig)
b=1
A=('greedy')
#A=('binary')
#F=('fast' 'basic')
F=('fast')
#R=('all' 'dense')
R=('dense')

for d in "${D[@]}"
do
    for a in "${A[@]}"
    do
		for f in "${F[@]}"
		do
			for r in "${R[@]}"
			do
				line="${d}.txt ${b} ${a} ${f} ${r}"
				str="${d}_${b}_${a}_${f}_${r}"
				out="./logs/"${str}"_char.out" 
				err="./logs/"${str}"_char.err" 
				log="./logs/"${str}"_char.log" 
				#echo -append \"arguments = \"${line}\"\" condor_description
				condor_submit -append "arguments = ${line}" -append "output = ${out}" -append "error = ${err}" -append "log = ${log}" condor_description  
			done
		done
	done
done
