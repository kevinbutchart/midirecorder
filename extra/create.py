#!/usr/bin/env python3

import mido
import time
import sys
import base64
from io import BytesIO
import pymongo

TICKS_PER_BEAT=480

BDR=36
SNR=38
CHH=44
OHH=46
RCY=59
HWB=76
OTR=81

input = [ { "_id" : 1, "name" : "metronome (4)", "beats" : 4, "pattern" : [ [OTR], [HWB], [HWB], [HWB] ] },
        { "_id" : 2, "name" : "metronome (3)", "beats" : 3, "pattern" : [ [OTR], [HWB], [HWB] ] },
        { "_id" : 3, "name" : "metronome (2)", "beats" : 2, "pattern" : [ [OTR], [HWB] ] },
        { "_id" : 4, "name" : "metronome (1)", "beats" : 1, "pattern" : [ [HWB] ] },
        { "_id" : 5, "name" : "Rock 8 beat", "beats" : 4, "pattern" : [ [RCY, BDR], [CHH], [CHH, SNR], [CHH, BDR],[CHH, BDR],[CHH], [CHH, SNR], [CHH] ] },
        { "_id" : 6, "name" : "Rock 16 beat", "beats" : 4, "pattern" : [ [RCY, BDR], [CHH], [CHH], [CHH], [CHH, SNR], [CHH], [CHH], [CHH, BDR],[CHH, BDR],[CHH],[CHH], [CHH], [CHH, SNR], [CHH], [CHH], [CHH] ] }
        ]

if __name__ == "__main__":
    dbclient = pymongo.MongoClient()
    db = dbclient["pianodb"]
    loops = db["loops"]
    for i in input:
        mid = mido.MidiFile()
        track = mido.MidiTrack(ticks_per_beat = TICKS_PER_BEAT)
        track.append(mido.MetaMessage('set_tempo', time=0, tempo=120))
        pattern = i["pattern"]
        beats = i["beats"]
        div = int(len(pattern) / beats)
        delay = int(TICKS_PER_BEAT / div)
        print(div)
        print(delay)
        time = 0
        tmplist = []
        for p in pattern:
            for n in p:
                tmplist.append(mido.Message('note_on', note=n, channel=9, time=time))
            time += delay

        lasttime = 0
        for m in tmplist:
            diff = m.time - lasttime
            lasttime = m.time
            m.time = diff
            track.append(m)

        track.append(mido.MetaMessage('end_of_track', time=delay))

        mid.tracks.append(track)

        b = BytesIO()
        mid.save(file=b)
        mid.save('out.mid')
        buf = b.getbuffer()
        out = base64.b64encode(buf).decode()
        output = i
        output["data"] = out
        print(output)
        query = { "_id" : output['_id'] }
        res = loops.replace_one(query, output, upsert = True)
        print(res)

