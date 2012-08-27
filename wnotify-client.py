import socket
import time
import os
from Tkinter import *


ADDRESS = "localhost"
PORT = 23567
PASSWORD = "er98vzt2945z42zt8j798z7TZ=/(Tn675ev5v6584553W$47e9876Tvl3py7"


prev_data = ""


def notifysend(data):
    root = Tk()

    w = Text(root, width=16, height=6)

    print dir(w)

    def click(arg):
        root.destroy()

    w.bind("<Double-Button-1>", click)

    w.insert(INSERT, data)


    w.config(state=DISABLED)
    w.pack()

    #root.geometry("{0}x{1}-10+10".format(500, 300))
    root.wm_attributes("-topmost", 1)
    root.mainloop()

def onecycle():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDRESS, PORT))

    s.settimeout(5)

    s.sendall( PASSWORD )

    return_data = s.recv(1024)
    s.close()

    global prev_data
    if return_data != prev_data:
        print "DATA RECEIVED!"
        print return_data
        #os.system("notify-send WeeChat \"%s\"" % return_data)  # not reliable!
        notifysend(return_data)
        prev_data = return_data

try:

    while True:
        try:
            onecycle()
        except Exception as e:
            print str(e)
        time.sleep(10)

except KeyboardInterrupt:
    print "\nUser killed the program!"

finally:
    print "Client killed!"
