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

TMP=/tmp/MidiRecorder/
mkdir -p "$TMP"

while true
do
	PORT=$(waitport)
	$CMD -p $PORT "$TMP"/rec.mid

	DATE=$(date +%F)
	DIR="$RECORDINGDIRECTORY"/"$DATE"
	if [ ! -d "$DIR" ]
	then
		mkdir -p "$DIR"
	fi
        FNAME="$DIR"/$(date +%Y_%m%d_%H%M%S)".mid"
        mv "$TMP"/rec.mid "$FNAME"
        createjson "$FNAME"
done

