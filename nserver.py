import SocketServer
import socket
import os

HOST, PORT = "localhost", 23567
PASSWORD = "er98vzt2945z42zt8j798z7TZ=/(Tn675ev5v6584553W$47e9876Tvl3py7"

PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0], "notify.txt")

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            self.handle_try()
        except:
            self.request.sendall( "ERROR" )
        finally:
            self.request.close()


    def handle_try(self):
        self.request.settimeout(5)

        ps = self.request.recv(60)
        if ps != PASSWORD:
            raise Exception("PERROR")

        fnotify = open(PATH)
        lines = fnotify.readlines()
        fnotify.close()

        lines = lines[-3:]
        self.request.sendall( "\n".join(lines) )

        fnotify = open(PATH, "w")
        fnotify.writelines(lines)
        fnotify.close()


class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.allow_reuse_address = True
        SocketServer.TCPServer.server_bind(self)


server = None
try:
    # Create the server, binding to host address and port
    server = MyTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print "\nUser killed the program!"

finally:
    if server != None:
        server.shutdown()
    print "Server killed!"
