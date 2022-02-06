#!/usr/bin/env python3

import sys
from traceback import print_exc

import dbus

def notify_new_recording(id):
    bus = dbus.SessionBus()

    try:
        remote_object = bus.get_object("com.gamoeba.recordingservice",
                                       "/ListenObject")

        iface = dbus.Interface(remote_object, "com.gamoeba.recordinginterface")
        iface.new_recording_available(id)
    except dbus.DBusException:
        print("can't notify new recording, service not available")
        

if __name__ == '__main__':
    notify_new_recording(57) 
