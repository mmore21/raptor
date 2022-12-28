#!/bin/bash


# Raptor Nmap Automation Script


if [ -z "$1" ]
then
	echo "Usage: ./raptor.sh <IP>"
	exit 1
fi


echo '                      __'
echo '____________  _______/  |_  ___________'
echo '\_  __ \__  \ \____ \   __\/  _ \_  __ \'
echo ' |  | \// __ \|  |_> >  | (  <_> )  | \/'
echo ' |__|  (____  /   __/|__|  \____/|__|'
echo '            \/|__|'


printf '                      __' > results
printf "\n" >> results
printf '____________  _______/  |_  ___________' >> results
printf "\n" >> results
printf '\_  __ \__  \ \____ \   __\/  _ \_  __ \' >> results
printf "\n" >> results
printf ' |  | \// __ \|  |_> >  | (  <_> )  | \/' >> results
printf "\n" >> results
printf ' |__|  (____  /   __/|__|  \____/|__|' >> results
printf "\n" >> results
printf '            \/|__|' >> results
printf "\n" >> results


printf "\n---- Raptor Autorecon ----\n\n" >> results
echo "---- Raptor Autorecon ----"


printf "\n---- Nmap TCP (Top 100) ----\n\n" >> results
echo "Running Nmap TCP (Top 100)..."
nmap $1 --top-ports 100 --open -oN nmap_tcp_100.txt >> results


printf "\n---- Nmap TCP (All) ----\n\n" >> results
echo "Running Nmap TCP (All)..."
nmap $1 -p- -sT -T4 --open -oN nmap_tcp_all.txt >> results

ports=""
while read line
do
	if [[ $line == *open* ]]
	then
		port=$(echo $line | awk -F'[^0-9]+' '{ print $1 }')
		ports="${ports},${port}"
	fi
done < nmap_tcp_all.txt

ports=$(echo $ports | sed 's/[^0-9]*//')
printf "\n---- Nmap TCP (Aggressive) ----\n\n" >> results
echo "Running Nmap TCP (Aggressive)..."
nmap $1 -p $ports -A -T4 --open -oN nmap_tcp_int.txt >> results

printf "\n---- Nmap UDP (Top 100) ----\n\n" >> results
echo "Running Nmap UDP (Top 100)..."
nmap $1 -sU -T4 --top-ports 100 --open -oN nmap_udp_100.txt >> results

while read line
do
	if [[ $line == *open* ]] && [[ $line == *http* ]]
	then
		port=$(echo $line | awk -F'[^0-9]+' '{ print $1 }')

		echo "Running Gobuster..."
		gobuster dir -u $1 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o gobuster_${port}.log -x php,html,txt -f -n -k >> temp1

		echo "Running WhatWeb..."
		whatweb $1 -v >> temp2
	fi
done < nmap_tcp_all.txt


if [ -e temp1 ]
then
	printf "\n---- Gobuster ----\n\n" >> results
	cat temp1 >> results
	rm temp1
fi


if [ -e temp2 ]
then
	printf "\n---- WhatWeb ----\n\n" >> results
	cat temp2 >> results
	rm temp2
fi


cat results
