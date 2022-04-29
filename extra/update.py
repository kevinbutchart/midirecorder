#!/usr/bin/env python3

import mido
import time
import sys
import base64
from datetime import datetime,timedelta
from io import BytesIO
import pymongo


if __name__ == "__main__":
    dbclient = pymongo.MongoClient()
    db = dbclient["pianodb"]
    recordings = db["recordings"]
    recs = recordings.find().sort("datetime", 1)
    session = datetime.min
    for rec in recs:
        dt = rec["datetime"]
        if dt - session > timedelta(0, 1800):
            session = dt
        rec["session"] = session

        query = { "_id": rec["_id"] }
        recordings.replace_one(query, rec)

        print(rec)
