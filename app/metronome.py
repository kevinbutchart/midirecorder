import asyncio, threading
import time
import mido
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage
from ordered_set import OrderedSet
import os

def led_on():
    os.system('ledon 1')

def led_off():
    os.system('ledon 0')

msgStrong = mido.Message('note_on', note=81, channel=9)
msg = mido.Message('note_on', note=76, channel=9)

class Metronome(threading.Thread):
    bpm = 80
    beats = 4
    volume = 80

    def set(self, bpm, beats, volume):
        self.should_exit = False
        self.bpm = int(bpm)
        self.beats = int(beats)
        self.volume = int(volume)

    def run(self):
        counter = 1
        output_ports = self.list_output_ports()
        if len(output_ports) > 0:
            self.start_metronome(output_ports[0])

    def start_metronome(self, port):
        with mido.open_output(port, autoreset=True) as outport:
            while not self.should_exit:
                delay = 60/self.bpm
                outport.send(msgStrong)
                outport.send(msg)
                time.sleep(delay)
                for i in range(1, self.beats):
                    outport.send(msg)
                    time.sleep(delay)

    def list_output_ports(self):
        ports = OrderedSet() 
        for port in mido.get_output_names():
            if "Through" not in port and "RPi" not in port and "RtMidi" not in port and "USB-USB" not in port:
                ports.append(port)
        return ports

    def stop(self):
        self.should_exit = True
