import asyncio, threading
import time
import mido
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage
from ordered_set import OrderedSet
from io import BytesIO
import os

def led_on():
    os.system('ledon 1')

def led_off():
    os.system('ledon 0')

class MidiPlayer(threading.Thread):
    def __init__(self, file=None, bytes=None):
        super().__init__()
        self.should_exit = False
        self.file = file
        if file == None and bytes != None:
            self.file = BytesIO(bytes)

    def run(self):
        counter = 1
        output_ports = self.list_output_ports()
        if len(output_ports) > 0:
            self.play_midi(output_ports[0])

    def play_midi(self, port):
        output_time_last = 0
        delay_debt = 0
        t0 = None
        led_on()
        with mido.open_output(port, autoreset=True) as outport:
            mid = mido.MidiFile(file=self.file)
            for message in mid:
                if self.should_exit:
                    break
                if(t0 == None):
                    t0 = time.time()
                    output_time_start = time.time()
                output_time_last = time.time() - output_time_start
                delay_temp = message.time - output_time_last
                delay = message.time - output_time_last - float(0.003) + delay_debt
                if(delay > 0):
                    time.sleep(delay)
                    delay_debt = 0
                else:
                    delay_debt += delay_temp
                output_time_start = time.time()

                if not message.is_meta:
                    outport.send(message)
            led_off()

    def list_output_ports(self):
        ports = OrderedSet() 
        for port in mido.get_output_names():
            if "Through" not in port and "RPi" not in port and "RtMidi" not in port and "USB-USB" not in port:
                ports.append(port)
        return ports

    def stop(self):
        self.should_exit = True
