#!/bin/bash
pids=(Chart Cli Closure Codec Collections Compress Csv Gson JacksonCore JacksonDatabind JacksonXml Jsoup JxPath Lang Math Mockito Time)
bids=(26 40 176 18 28 47 16 18 26 112 6 93 22 65 106 38 27)
for i in {0..16}
do
	for((j=1;j<=${bids[i]};j++));
	do
		if [[ Cli == ${pids[i]} ]] && [[ 6 == ${j} ]]; then
			continue
		fi
		if [[ Collections == ${pids[i]} ]] &&  [[ 25 > ${j} ]]; then
			continue
		fi
		if [[ Closure == ${pids[i]} ]] &&  [[ 63 == ${j} || 93 == ${j} ]]; then
			continue
		fi
		if [[ Lang == ${pids[i]} ]] &&  [[ 2 == ${j} ]]; then
			continue
		fi
		if [[ Time == ${pids[i]} ]] &&  [[ 21 == ${j} ]]; then
			continue
		fi
		defects4j checkout -p ${pids[i]} -v ${j}b -w /home/ubuntu/BugLocator/${pids[i]}_${j}_buggy 
		cd /home/ubuntu/BugLocator/${pids[i]}_${j}_buggy 
		path=$(defects4j export -p dir.src.classes)
		java -jar /home/ubuntu/BugLocator/BugLocator.jar -b /home/ubuntu/BugLocator/XML/${pids[i]}/${j}.xml -s /home/ubuntu/BugLocator/${pids[i]}_${j}_buggy/${path} -a 0.2 -o /home/ubuntu/BugLocator/Results/${pids[i]}/${j}
		cd ..
		rm -rf /home/ubuntu/BugLocator/${pids[i]}_${j}_buggy 
	done
done