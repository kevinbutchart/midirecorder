#!/usr/bin/env python3
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import subprocess
from midirecordingsdb import MidiRecordingsDB
from midiplayer import MidiPlayer
from metronome import Metronome
from connectionmanager import ConnectionManager
from pathlib import Path
import asyncio
import uvicorn
import json
import tempfile
import queue
import base64
from filewatcher import FileWatcher

from os.path import dirname, join

current_dir = dirname(__file__)
template_dir = join(current_dir, 'templates')

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")
templates = Jinja2Templates(directory=template_dir)
j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
db = MidiRecordingsDB()
#midirecorder = MidiRecorder(db)
metronome = Metronome()

@app.on_event('startup')
async def app_startup():
    print("starting")

@app.on_event('shutdown')
async def app_shutdown():
    print("in app shutdown")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    recs = db.get_recordings_by_date(limit=150)
    return templates.TemplateResponse("main.html", {"request" : request, "recordings": recs})

@app.get("/rhythm", response_class=HTMLResponse)
async def get_rhythm(request: Request):
    settings = db.get_metronome_settings()
    return templates.TemplateResponse("rhythm.html", {"request" : request, "settings" : settings})


def midi_to_audio(infile, outfile):
    subprocess.call(['fluidsynth', '-ni', './Yamaha.sf2', infile, '-F', outfile, '-r', '44100', '-g', '0.5'])


@app.get("/recording/{id}", response_class=HTMLResponse)
async def get_recording(request: Request, background_tasks: BackgroundTasks, id):
    rec = db.get_recording(id)
    return templates.TemplateResponse("recording.html", {"request" : request, "rec" : rec})

manager = ConnectionManager()

class CommandRunner():

    def __init__(self):
        self.midiplayer = None

        self.commands = { "play" : self.play,
                    "stop" : self.stop,
                    "start_metronome" : self.start_metronome,
                    "update_metronome" : self.update_metronome,
                    "stop_metronome" : self.stop_metronome,
                    "set_title" : self.set_title,
                    "set_favourite" : self.set_favourite
                    }

    def run(self, message):
        cmd = self.commands[ message['command'] ]
        if cmd is not None:
            cmd(message)

    def play(self, message):
        print(message, flush=True)
        id = message['id']
        rec = db.get_recording(id)
        if self.midiplayer != None:
            self.midiplayer.stop()
        midfile = base64.b64decode(rec["data"])
        self.midiplayer = MidiPlayer(bytes = midfile)
        self.midiplayer.start()

    def stop(self, message):
        self.midiplayer.stop()
        self.midiplayer = None

    def update_metronome(self, message):
        message['loop_id'] = 1
        db.set_metronome_settings(message)
        metronome.update_metronome()

    def start_metronome(self, message):
        metronome.start_metronome()
        if not metronome.is_alive():
            metronome.start()

    def stop_metronome(self, message):
        metronome.stop_metronome()

    def set_title(self, message):
        id = message['id']
        title = message['title']
        rec = db.get_recording(id)
        print (id)
        print (rec)
        print(title)
        rec.title = title
        db.commit()

    def set_favourite(self, message):
        id = message['id']
        favourite = message['favourite']


async def consumer_handler(websocket):
    cmd_runner = CommandRunner()
    while True:
        message = await websocket.receive_text()
        print(message)
        message = json.loads(message)
        cmd_runner.run(message)

async def producer_handler(websocket):
    while True:
        msg = await msg_queue.get()
        msg_content = json.loads(msg)
        print(msg_content)
        if msg_content['msg'] == 'new_recording':
            print('new_rec_received')
            cmd = { 'command' : 'reload' }
            cmdstr = json.dumps(cmd)
            await websocket.send_text(cmdstr)

@app.websocket("/main")
async def websocket_main(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        global msg_queue
        msg_queue = asyncio.Queue()
        FileWatcher(msg_queue)
        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket))
        producer_task = asyncio.ensure_future(
            producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    print("Disconnecting socket")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
