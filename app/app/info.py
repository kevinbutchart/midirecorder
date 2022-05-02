#!/usr/bin/env python3
import base64
import pymongo

dbclient = pymongo.MongoClient("mongodb://pianorecorder-database-1")
db = dbclient["pianodb"]
call = db.command("dbstats")
database = call['db']
datasize = call['dataSize'] / (1024 * 1024)
objects = call['objects']
collections = call['collections']

print('\n')
print('Database:', str(database))
print('Objects:', str(objects))
print('Collections:', str(collections))
print('Size:', str(datasize) + 'Mb')
print('\n')
