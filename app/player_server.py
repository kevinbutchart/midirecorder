#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from metronome import Metronome

metronome = Metronome()
metronome.start()

PORT = 9900  # The port used by the server

class Server(protocol.Protocol):
    def dataReceived(self, data):
        msg = data.decode()
        cmd = msg.strip().split(' ')
        print(cmd)
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
        self.transport.write("ok\n".encode())

class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Server()

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:"+str(PORT)).listen(ServerFactory())
    reactor.run()
