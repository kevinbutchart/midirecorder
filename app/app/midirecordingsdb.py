from datetime import datetime, timedelta
import time
from pprint import pprint
from collections import OrderedDict
import os
import sys
import base64

import pymongo

from bson.objectid import ObjectId

db_url = 'mongodb://pianodb'
#db_url = "mongodb+srv://kevinbutchart:<pw>@cluster0.hgww9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

class MidiRecordingsDB:
    def __init__(self):
        dbclient = pymongo.MongoClient(db_url)
        self.db = dbclient["pianodb"]
        self.recordings = self.db["recordings"]
        self.settings = self.db["settings"]
        self.loops = self.db["loops"]
        self.tags = self.db["tags"]
        self.recordings.create_index("datetime")

    def get_recording(self, id):
        print(id)
        query={"_id":ObjectId(id)}
        res=self.recordings.find_one(query)
        print(res)
        return res

    def get_last_recording(self):
        return self.recordings.find_one(sort=[("datetime", -1)])

    def add_recording_int(self, record):
        id = self.recordings.insert_one(record)
        return id

    def add_recording(self, data, duration):
        title = ''
        date_time_obj = datetime.utcnow()
        name = date_time_obj.strftime("%Y_%m%d_%H%M%S.mid")
        duration = duration
        favourite = False
        session = date_time_obj
        last_rec = self.get_last_recording()
        print(last_rec)
        if last_rec:
            delta = date_time_obj - last_rec["datetime"]
            print(delta)
            if delta < timedelta(0, 1800):
                print("use current session")
                session = last_rec["session"]

        new_recording =  {"title": title,
                          "name": name,
                          "datetime": date_time_obj,
                          "duration": duration,
                          "session" : session,
                          "favourite": favourite,
                          "data" : base64.b64encode(data)}
        id = self.recordings.insert_one(new_recording)
        return id

    def get_recordings_by_date(self, limit = 0):
        recordings_dict = OrderedDict()
        query = self.recordings.find().sort("datetime", -1).limit(0)

        for instance in query:
            date = instance["datetime"].date()
            day_recordings = recordings_dict.get(date, [])
            day_recordings.append( instance )
            recordings_dict[date] = day_recordings
        return recordings_dict

    def get_recording_sessions(self, limit = 0):
        recordings_dict = OrderedDict()
        query = self.recordings.find().sort("datetime", -1).limit(limit)

        for instance in query:
            session = instance["session"]
            session_recordings = recordings_dict.get(session, [])
            session_recordings.append( instance )
            recordings_dict[session] = session_recordings
        return recordings_dict

    def get_loops(self, beats):
        query = { "beats" : beats}
        return self.loops.find(query)

    def get_tags(self):
        return self.tags.find()

    def get_loop(self, id):
        query = { "_id" : id }
        return self.loops.find_one(query)

    def get_metronome_settings(self):
        query = { "_id" : "metronome" }
        return self.settings.find_one(query)

    def set_metronome_settings(self, settings):
        query = { '_id' : "metronome" }
        self.settings.replace_one(query, settings, upsert=True)

if __name__ == '__main__':
    db = MidiRecordingsDB()
    recs = db.get_recordings_by_date(250)
    pprint(recs)
