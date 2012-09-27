import time
import os
import json


def get_real_path():
    abspath = os.path.abspath(__file__)
    if os.path.islink(abspath):
        return os.readlink(abspath)
    else:
        return abspath

prefix = os.path.dirname(get_real_path())
config = json.load(open(os.path.join(prefix, "wnserver.conf")))

try:
    import weechat
    import string

    TIME_FORMAT = config["timeformat"]

    weechat.register(
        'wnotify',
        '',
        '2.0',
        'GPL',
        'WeeChat script for writing notification messages to file.',
        '',
        ''
    )

    weechat.hook_signal('weechat_pv', 'on_priv', '')
    weechat.hook_signal('weechat_highlight', 'on_highlight', '')

    notify_txt = os.path.join(prefix, config["notifyfile"])

    def on_highlight(data, signal, signal_data):
        append_notification(signal_data)
        return weechat.WEECHAT_RC_OK

    def on_priv(data, signal, signal_data):
        append_notification(signal_data)
        return weechat.WEECHAT_RC_OK

    def append_notification(message):
        notifyfile = open(notify_txt, "a")
        message = message if len(message) <= config["linelimit"] else \
            "{0}...".format(message[:config["linelimit"]])
        message = string.replace(message, "\t", ": ", 1)
        notifyfile.write("{0} {1}\n".format(
            time.strftime(TIME_FORMAT, time.localtime()),
            message
        ))
        notifyfile.close()


except ImportError:
    import SocketServer
    import ssl
    import socket

    notify_txt = os.path.join(prefix, config["notifyfile"])

    if config["password"] is "changeme":
        print "Change the password in 'wnserver.conf' file"

    class MyTCPHandler(SocketServer.BaseRequestHandler):

        def handle(self):
            try:
                self.handle_try()
            except Exception as e:
                log = open(config["logfile"], "a")
                log.write("{0}: {1}".format(str(time.time()), str(e)))
                log.close()
                print str(e)
            finally:
                self.request.close()

        def handle_try(self):
            self.request.settimeout(5)

            ps = self.request.recv(len(config["password"]))
            if ps != config["password"]:
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
                certfile=os.path.join(prefix, config["certfile"]),
                keyfile=os.path.join(prefix, config["keyfile"])
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
        server = MyTCPServer((config["address"], config["port"]), MyTCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "\nUser killed the program!"

    finally:
        if server is not None:
            server.shutdown()
        print "Server killed!"
