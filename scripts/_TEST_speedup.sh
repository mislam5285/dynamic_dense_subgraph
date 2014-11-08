#!/bin/bash
#D=(tumblr students enron facebook twitter)
#D=(facebookBig twitterBig facebook twitter)

# datasets to use
D=(twitterBig facebookBig)

# timebudget in days
b=1

# type of algorithm (greedy or binary)
A=('greedy')
#A=('binary')

# variant of algorithm (with if without speedup)
#F=('fast' 'basic')
F=('fast')

# run on whole graph or only in the densest subgraph
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
				out="${str}_speedup.out"
				python ./../scripts/main_speedup.py "${line}" > "${out}"
			done
		done
	done
done
