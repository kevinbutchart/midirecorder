#!/usr/bin/env python3
import socket

import mido
import time
import json
import queue
import threading

from tcpconnection import TcpConnection

playQueue = queue.Queue()

def get_ms():
    return round(time.time_ns() / 1_000_000)


def player():
    output_ports=mido.get_output_names()
    port_name = output_ports[1]

    oport = mido.open_output(port_name)
    print("start thread")
    time.sleep(.25)
    print("start playback")
    start_time = get_ms()
    while True:
        msg = playQueue.get()
        print(msg)
        play_time = (get_ms() - start_time)/1_000
        if msg.time > play_time:
            time.sleep(msg.time - play_time)
        oport.send(msg)
        print(f'{msg}')

def clientfn(conn):
    max_diff = - 1_000_000
    min_diff = 1_000_000
    connect_ms = 0 
    while True:
        rmsg = conn.recv(128)
        if connect_ms == 0:
            connect_ms = get_ms()
            threading.Thread(target=player, daemon=True).start()
        messages = [ rmsg[i:i+8] for i in range(0, len(rmsg), 8) ]
        for msg in messages:
            if len(msg) != 8:
                print(len(msg))
            if msg[0] != 255:
                print("bad messge")
                break
            ms = int.from_bytes(msg[1:5], byteorder='big')
            local_ms = get_ms() - connect_ms
            print(local_ms)
            diff = local_ms - ms
            if diff > max_diff:
                max_diff = diff
            if diff < min_diff:
                min_diff = diff
            print(f"diff {diff} min: {min_diff} max: {max_diff}")
            
            msg = mido.Message.from_bytes(msg[5:8])
            msg.time = ms / 1_000
            playQueue.put(msg)
            print(msg)
            #oport.send(msg)


HOST = "kbserver21.hopto.org"  # The server's hostname or IP address
PORT = 9900  # The port used by the server


conn = TcpConnection(HOST, PORT)
conn.connect(clientfn)
