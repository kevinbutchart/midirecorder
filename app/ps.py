#!/usr/bin/env python3
import socket

import mido
import time
import json
from tcpconnection import TcpConnection
from metronome import Metronome

metronome = Metronome()
metronome.start()

def server_fn(conn):
    while True:
        msg = conn.makefile().readline()
        cmd = msg.strip().split(' ')
        if cmd[0] == 'metronome':
            if len(cmd) == 2:
                result = 'ok\n'.encode()
                subcmd = cmd[1]
                if subcmd == 'start':
                    metronome.start_metronome()
                    conn.send(result)
                    continue
                if subcmd == 'update':
                    metronome.update_metronome()
                    conn.send(result)
                    continue
                if subcmd == 'stop':
                    metronome.stop_metronome()
                    conn.send(result)
                    continue

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 9900  # The port used by the server

if __name__ == '__main__':
    conn = TcpConnection(HOST, PORT)
    conn.start_server(server_fn)
