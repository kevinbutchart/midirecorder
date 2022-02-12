#!/usr/bin/env python3
import asyncio, threading
import time
import posix
from midirecordingsdb import MidiRecordingsDB
from midiplayer import MidiPlayer
from subprocess import call
import time
import random
import sys
import os
import errno
import datetime
import psutil
import fcntl
import socket
import mido
import queue
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage
from pprint import pprint
import argparse
import threading
from ordered_set import OrderedSet
from io import BytesIO
import setproctitle

from midiplayer import MidiPlayer

import os
import signal
import sys
import time

def writeToLog(msg):
    logfile = open("/tmp/state.log","a")
    logfile.write(str(msg) + "\n")
    logfile.close()

def led_on():
    os.system('ledon 1')

def led_off():
    os.system('ledon 0')


def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)

global last_recording
last_recording = None


BPM=120
TICKS_PER_BEAT=480
class RecordMidi():
    def __init__(self):
        self.is_recording = False
        self.recording = []
        self.start_time = 0
        self.last_time = 0
        self.state = {
                "keys" : set(),
                "pedals" : set() 
        }
        self.damper_val = 0
        self.should_exit = False
        self.player = None
        self.message_queue = queue.Queue()

    def list_input_ports(self):
        ports = OrderedSet() 
        for port in mido.get_input_names():
            if "Through" not in port and "RPi" not in port and "RtMidi" not in port and "USB-USB" not in port:
                ports.append(port)
        return ports

    def calc_time_delta(self):
        current_time = time.time()
        if self.last_time == 0:
            self.last_time = current_time
        delta = current_time - self.last_time
        self.last_time = time.time()
        return delta

    def __receive_messages(self, message):
        if message.type != 'clock':
            self.message_queue.put(message.copy(time=self.calc_time_delta()))

    def start_record(self, port):
        writeToLog("wait start")
        global last_recording
        self.is_recording = False
        inport = None 
        self.last_time = time.time()
        with mido.open_input(port, callback=self.__receive_messages) as inport:
            while not self.is_recording:
                while not self.message_queue.empty():
                    msg = self.message_queue.get()
                    if not self.is_recording:
                        if msg.type == 'note_on' and msg.note != 108:
                            self.is_recording = True
                            self.start_time = time.time()
                            # override delta time on first note as we always want the recording to start immediately
                            self.__add_msg(msg.copy(time=0))
                            if self.damper_val > 0:
                                self.__add_msg(Message('control_change', control=64, value=self.damper_val, time=0))
                            break
                        else:
                            if (msg.is_cc(66) and msg.value == 0) or (msg.type == 'note_off' and msg.note == 108):
                                if last_recording is not None:
                                    if self.player is None or not self.player.is_alive():
                                        self.player = MidiPlayer(bytes=last_recording)
                                        self.player.start()
                                    else:
                                        self.player.stop()
                                        self.player = None
                            if msg.is_cc(64):
                                self.damper_val = msg.value

                time.sleep(0.1)
                # safety catch - if radio silence for more than 3600 seconds, restart listening
                if time.time() - self.last_time > 3600 and (self.player == None or not self.player.is_alive()):
                    self.should_exit = True 
                if self.should_exit:
                    return None

            if self.player != None:
                led_off()
                self.player.stop()
                self.player = None
                return None
            writeToLog("start record loop")
            led_on()
            while self.is_recording and not self.should_exit:
                while not self.message_queue.empty():
                    msg = self.message_queue.get()
                    self.__add_msg(msg)

                if time.time() - self.last_time > 3 and self.__is_inactive():
                    self.is_recording = False 
                # safety catch - abort all recording if silent for 30 seconds
                if time.time() - self.last_time > 30:
                    self.is_recording = False 
                time.sleep(.1)
            writeToLog("exit record loop")
            led_off()

            if self.should_exit:
                return None

            writeToLog("before write")

            mid = MidiFile()
            track = MidiTrack(ticks_per_beat = TICKS_PER_BEAT)
            mid.tracks.append(track)

            tempo = mido.bpm2tempo(BPM)
            for msg in self.recording:
                track.append(msg.copy(time = round(mido.second2tick(msg.time, TICKS_PER_BEAT, tempo))))

            b = BytesIO()
            mid.save(file=b)
            last_recording = b.getbuffer()
            writeToLog("after write")
            resp =  { 'bytes' : b.getbuffer(), 'duration' : mid.length}
            writeToLog(resp)
            return resp
        return None 

    def __add_msg(self, msg):
        self.recording.append(msg)
        self.__update_state(msg)

    def __update_state(self, msg):
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            print("discarding " + str(msg.note))
            self.state['keys'].discard(msg.note)
        else:
            if msg.type == 'note_on':
                self.state['keys'].add(msg.note)
        if msg.is_cc():
            if msg.control in [64, 66, 67]:
                if msg.value > 32:
                    self.state['pedals'].add(msg.control)
                else:
                    self.state['pedals'].discard(msg.control)

    def __is_inactive(self):
        inactive =  self.state['keys'] == set() and self.state['pedals'] == set()
        if inactive == False:
            print("pedals")
            print(self.state['pedals'])
            print("keys")
            print(self.state['keys'])
        return inactive

class MidiRecorder():
    def __init__(self, db):
        super().__init__()
        self.db = db 
        self.rm = None

    def run(self):
        while True:
            self.rm = RecordMidi()
            input_ports = self.rm.list_input_ports()
            while len(input_ports) == 0:
                writeToLog(len(input_ports))
                time.sleep(1)
                input_ports = self.rm.list_input_ports()

            print("Recording on: " + input_ports[0])
            writeToLog("Recording on " + input_ports[0])
            msg = self.rm.start_record(input_ports[0])
            if msg != None and msg['duration'] > 0.1:
                rec_id = self.db.add_recording(msg['bytes'], msg['duration'])
                #dbus_client.notify_new_recording(rec_id)

if __name__ == "__main__":
    setproctitle.setproctitle('midirecorder')
    signal.signal(signal.SIGUSR1, handle_pdb)
    print(f"Started process: {os.getpid()}")
    db = MidiRecordingsDB('sqlite:///./recordings.db')
    midirecorder = MidiRecorder(db)
    midirecorder.run()
