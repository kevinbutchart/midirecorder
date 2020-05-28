#!/bin/bash

RECORDINGDIRECTORY=/var/www/html/midi/

# first setup a few things
disablemmcled

while true
do
	DATE=$(date +%F)
	DIR="$RECORDINGDIRECTORY"/"$DATE"
	if [ ! -d "$DIR" ]
	then
		mkdir -p "$DIR"
	fi
	index=0
	FILES=$(ls "$DIR"/*.mid) && {
	   index=$(echo $FILES | xargs basename -a | while read r;do echo ${r%_*};done | sort -r -n | head -n 1)
        }
	((index=index + 1))
	arecsplitmidi -p 20:0 "$DIR"/"$index"_"$DATE".mid
done

