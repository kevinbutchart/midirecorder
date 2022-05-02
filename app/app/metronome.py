import asyncio, threading
import time
import mido
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage
from midirecordingsdb import MidiRecordingsDB
from ordered_set import OrderedSet
import os
import base64
from io import BytesIO


class Metronome(threading.Thread):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(Metronome, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super(Metronome, self).__init__()
        self.db = MidiRecordingsDB()
        self.should_exit = False
        self.metronome_on = False
        self.settings = self.db.get_metronome_settings()
        if not self.settings:
            self.settings = {'bpm':80, 'beats':4, 'volume': 60, 'loop_id': 1 }
            self.db.set_metronome_settings(self.settings)

    def start_metronome(self):
        self.metronome_on = True
        self.update = True

    def update_metronome(self):
        self.update = True

    def stop_metronome(self):
        self.metronome_on = False

    def run(self):
        while not self.should_exit:
            if self.metronome_on:
                output_ports = self.list_output_ports()
                if len(output_ports) > 0:
                    port = output_ports[0]
                    with mido.open_output(port, autoreset=True) as outport:
                        self.play_loop(outport)
            time.sleep(.2)

    def play_loop(self, port):
        while self.metronome_on:
            self.settings = self.db.get_metronome_settings()
            self.update = False
            loop_info = self.db.get_loop(self.settings['loop_id'])
            file = BytesIO(base64.b64decode(loop_info['data']))
            mid = mido.MidiFile(file=file)
            tempo = int((60 * 1000 * 1000) / int(self.settings['bpm']))
            for i, track in enumerate(mid.tracks):
                for j, msg in enumerate(track):
                    if msg.type == 'set_tempo':
                        print(tempo)
                        msg.tempo = tempo
                        track[j] = msg

            volume = int(self.settings['volume'])
            volmsg = mido.Message('control_change', channel=9, control=7, value=volume)
            port.send(volmsg)
            while self.metronome_on and not self.update:
                for msg in mid.play():
                    if not self.metronome_on:
                        break
                    port.send(msg)

    def list_output_ports(self):
        ports = OrderedSet()
        for port in mido.get_output_names():
            if "Through" not in port and "RPi" not in port and "RtMidi" not in port and "USB-USB" not in port:
                ports.append(port)
        return ports

    def stop(self):
        self.stop_metronome()
        self.should_exit = True
