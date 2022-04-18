#!/usr/bin/env python3
from twisted.internet import protocol, reactor, endpoints
from metronome import Metronome

metronome = Metronome()
metronome.start()


HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 9900  # The port used by the server

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        msg = data.decode()
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
        self.transport.write("ok\n".encode())

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__ == '__main__':
    endpoints.serverFromString(reactor, "tcp:"+str(PORT)).listen(EchoFactory())
    reactor.run()
