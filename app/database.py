#!/usr/bin/env python3
import pymongo
print("one")
dbclient = pymongo.MongoClient("mongodb://pianorecorder_database_1")
print(dbclient)
db = dbclient["testrec"]
print(db)
recordings = db["recordings"]
print(recordings)
mydict = { "name": "John", "address": "Highway 37" }
ins = recordings.insert_one(mydict)
print(ins)

res = recordings.find()
for x in res:
    print(x)
