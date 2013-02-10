import ssl
import socket
import time
import mynotify
import os
import json


def get_real_path():
    abspath = os.path.abspath(__file__)
    if os.path.islink(abspath):
        return os.readlink(abspath)
    else:
        return abspath

prefix = os.path.dirname(get_real_path())
prev_data = ""
myn = mynotify.Notification()
config = json.load(open(os.path.join(prefix, "wnclient.conf")))

if config["password"] == "changeme":
    raise Exception("Change the password in 'wnclient.conf' file!")


def onecycle():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s)
    s.connect((config["address"], config["port"]))

    s.settimeout(config["timeout"])

    s.sendall(config["password"])

    return_data = s.recv(512)
    s.close()

    global prev_data
    if return_data != prev_data:
        print "DATA RECEIVED!"
        print return_data
        #os.system("notify-send WeeChat \"%s\"" % return_data)  # not reliable!
        myn.notify(
            "WeeChat",
            return_data,
            colors=config["colors"],
            size_heading=config["size_heading"],
            size_text=config["size_text"]
        )
        prev_data = return_data


try:
    while True:
        try:
            onecycle()
        except Exception as e:
            print str(e)
        time.sleep(config["interval"])

except KeyboardInterrupt:
    print "\nUser killed the program!"

finally:
    print "Client killed!"
