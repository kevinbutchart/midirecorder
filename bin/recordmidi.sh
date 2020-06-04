#!/bin/bash

RECORDINGDIRECTORY=/var/www/html/midi/
CMD=arecsplitmidi

getport() {
    $CMD -l | tail -n +2 | grep -v "Midi Through" | head -n 1 | awk '{print $1}'
}

waitport() {
    PORT=""
    while [ -z "$PORT" ]
    do
        PORT=$(getport)
        if [ -z $PORT ]
        then
            echo "waiting"
            sleep 1
        fi
    done
    echo $PORT
}

# first setup a few things
disablemmcled

while true
do
	PORT=$(waitport)
        echo "PORT: $PORT"
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
	$CMD -p $PORT "$DIR"/"$index"_"$DATE".mid
done

