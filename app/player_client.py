#!/usr/bin/env python3
import socket

import mido
import time
import json
import queue
import threading

HOST = "pianorecorder_pianorecorder_1"  # The server's hostname or IP address
PORT = 9900  # The port used by the server

class MidiPlayClient:

    def send_message(self, str):
        res = False
        str = str + '\n'
        msgbytes = str.encode()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(msgbytes)
            res = s.makefile().readline().strip() == 'ok'
            s.close()
        return res

    def start_metronome(self):
        return self.send_message("metronome start")

    def update_metronome(self):
        return self.send_message("metronome update")

    def stop_metronome(self):
        return self.send_message("metronome stop")
