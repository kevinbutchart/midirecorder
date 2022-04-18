#!/usr/bin/env python3
import socket

import mido
import time
import json

class TcpConnection():

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, clientfn):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            clientfn(s)

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        return s

    def start_server(self, serverfn):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    serverfn(conn)
