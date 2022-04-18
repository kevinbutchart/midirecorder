#!/usr/bin/env python3
import socket

HOST = "pianorecorder_midiplayer_1"  # The server's hostname or IP address
PORT = 9900  # The port used by the server

class MidiPlayClient:

    def send_message(str):
        res = False
        str = str + '\n'
        msgbytes = str.encode()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(msgbytes)
            res = s.makefile().readline().strip() == 'ok'
            s.close()
        return res

    def start_metronome():
        return MidiPlayClient.send_message("metronome start")

    def update_metronome():
        return MidiPlayClient.send_message("metronome update")

    def stop_metronome():
        return MidiPlayClient.send_message("metronome stop")
