#!/usr/bin/env python3

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib
import threading
import json

class ListenObject(dbus.service.Object):
    msg_queue = None

    @dbus.service.method("com.gamoeba.recordinginterface",
                         in_signature='t', out_signature='')
    def new_recording_available(self, id):
        print(f'new recording available {id}')
        if self.msg_queue is not None:
            print('sending')
            new_rec = {'msg' : 'new_recording', 'id' : id }
            msg = json.dumps(new_rec)
            print(msg)
            self.msg_queue.put_nowait(msg)
            print('sent')

class DBusThread (threading.Thread):
    def __init__(self, msg_queue):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue 

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("com.gamoeba.recordingservice", session_bus)
        object = ListenObject(session_bus, '/ListenObject')
        object.msg_queue = self.msg_queue

        mainloop = GLib.MainLoop()
        print("Running recording listening service")
        mainloop.run()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.gamoeba.recordingservice", session_bus)
    object = ListenObject(session_bus, '/ListenObject')

    mainloop = GLib.MainLoop()
    print("Running recording listening service")
    mainloop.run()
