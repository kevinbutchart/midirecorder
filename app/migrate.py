#!/usr/bin/env python3
from olddb import MidiRecordingsDB as OldDB 
from midirecordingsdb import MidiRecordingsDB
import base64

olddb = OldDB("sqlite:///./recordings.db") 
newdb = MidiRecordingsDB("mongodb://pianorecorder_database_1")
recs = olddb.get_recordings()

for r in recs:
    print(r)
    new_recording =  {"title": r.title,
                      "name": r.name, 
                      "datetime": r.datetime,
                      "duration": r.duration, 
                      "favourite": r.favourite, 
                      "data" : base64.b64encode(r.data.data)}
    print(new_recording)
    newdb.add_recording_int(new_recording)
