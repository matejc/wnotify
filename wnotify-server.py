import time

try:
    import weechat
    import os

    TIME_FORMAT = "[%H:%M]"

    weechat.register('wnotify', '', '1.4', 'GPL', 'WeeChat script for writing notification messages to file.', '', '')

    weechat.hook_signal('weechat_pv', 'on_priv', '')
    weechat.hook_signal('weechat_highlight', 'on_highlight', '')

    notify_txt = os.path.join(os.path.split(os.path.abspath(__file__))[0], "notify.txt")

    def on_highlight(data, signal, signal_data):
        append_notification(signal_data)
        return weechat.WEECHAT_RC_OK

    def on_priv(data, signal, signal_data):
        append_notification(signal_data)
        return weechat.WEECHAT_RC_OK

    def append_notification(message):
        notifyfile = open(notify_txt, "a")
        notifyfile.write("{0}	{1}\n".format(
            time.strftime(TIME_FORMAT, time.localtime()),
            message
        ))
        notifyfile.close()


except ImportError:
    import SocketServer
    import os
    import ssl
    import socket

    HOST, PORT = "localhost", 23567
    PASSWORD = "er98vzt2945z42zt8j798z7TZ=/(Tn675ev5v6584553W$47e9876Tvl3py7"

    PATH = os.path.split(os.path.abspath(__file__))[0]

    notify_txt = os.path.join(PATH, "notify.txt")

    class MyTCPHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            try:
                self.handle_try()
            except Exception as e:
                log = open("/tmp/wnotify-server.log", "a")
                log.write("{0}: {1}".format(str(time.time()), str(e)))
                log.close()
                print str(e)
            finally:
                self.request.close()

        def handle_try(self):
            self.request.settimeout(5)

            ps = self.request.recv(60)
            if ps != PASSWORD:
                raise Exception("PERROR")

            fnotify = open(notify_txt)
            lines = fnotify.readlines()
            fnotify.close()

            lines = lines[-3:]
            self.request.sendall("\n".join(lines))

            fnotify = open(notify_txt, "w")
            fnotify.writelines(lines)
            fnotify.close()

    class MyTCPServer(SocketServer.TCPServer):

        def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
            # See SocketServer.TCPServer.__init__
            # (added ssl-support):
            SocketServer.BaseServer.__init__(
                self, server_address, RequestHandlerClass
            )
            self.socket = ssl.wrap_socket(
                socket.socket(self.address_family, self.socket_type),
                server_side=True,
                certfile=os.path.join(PATH, "server.crt"),
                keyfile=os.path.join(PATH, "server.key")
            )

            if bind_and_activate:
                self.server_bind()
                self.server_activate()

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
