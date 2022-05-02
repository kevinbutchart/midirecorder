#!/bin/bash
inotifywait -r -m -e create /var/www/html/midi |
while read dirname eventlist eventfile
do
   [[ "$eventfile" =~ .*json$ ]] && {
       filedate=$(basename "$dirname")
       midifile=$(basename "$eventfile" .json).mid
       dropbox_uploader.sh upload "$dirname"/"$eventfile" /"$filedate"/"$eventfile"
       dropbox_uploader.sh upload "$dirname"/"$midifile" /"$filedate"/"$midifile"
   }
done
