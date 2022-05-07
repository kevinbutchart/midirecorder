#!/usr/bin/env python3

import time
import sys
import base64
from io import BytesIO
import pymongo

input = [ { "_id" : "moonbeams", "name" : "Moonbeams" },
        { "_id" : "bach_prelude_c_minor", "name" : "Prelude in C minor, BWV 999" },
        { "_id" : "peters_theme", "name" : "Peter's Theme" },
        { "_id" : "hearsay", "name" : "I hear what you say" },
        ]

if __name__ == "__main__":
    dbclient = pymongo.MongoClient()
    db = dbclient["pianodb"]
    tags = db["tags"]
    for i in input:
        query = { "_id" : i['_id'] }
        res = tags.replace_one(query, i, upsert = True)
        print(res)
