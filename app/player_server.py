#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from metronome import Metronome
from midirecordingsdb import MidiRecordingsDB
from midiplayer import MidiPlayer
import base64

metronome = Metronome()
metronome.start()
db = MidiRecordingsDB()
player = None

PORT = 9900  # The port used by the server

class Server(protocol.Protocol):
    def dataReceived(self, data):
        global player
        global metronome
        msg = data.decode()
        print(msg)
        cmd = msg.strip().split(' ')
        if cmd[0] == 'metronome':
            if len(cmd) == 2:
                result = 'ok\n'.encode()
                subcmd = cmd[1]
                if subcmd == 'start':
                    metronome.start_metronome()
                if subcmd == 'update':
                    metronome.update_metronome()
                if subcmd == 'stop':
                    metronome.stop_metronome()
        if cmd[0] == 'player':
            if cmd[1] == 'play':
                id = cmd[2]
                rec = db.get_recording(id)
                if player != None:
                    player.stop()
                midfile = base64.b64decode(rec["data"])
                player = MidiPlayer(bytes = midfile)
                player.start()
            if cmd[1] == 'stop':
                if player != None:
                   player.stop()
                player = None

        self.transport.write("ok\n".encode())

class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Server()

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:"+str(PORT)).listen(ServerFactory())
    reactor.run()
