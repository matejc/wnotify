import socket
import time
import mynotify

ADDRESS = "localhost"
PORT = 23567
PASSWORD = "er98vzt2945z42zt8j798z7TZ=/(Tn675ev5v6584553W$47e9876Tvl3py7"

prev_data = ""
myn = mynotify.Notification()


def onecycle():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDRESS, PORT))

    s.settimeout(5)

    s.sendall(PASSWORD)

    return_data = s.recv(1024)
    s.close()

    global prev_data
    if return_data != prev_data:
        print "DATA RECEIVED!"
        print return_data
        #os.system("notify-send WeeChat \"%s\"" % return_data)  # not reliable!
        myn.notify("WeeChat", return_data, mynotify.Notification.N_BLUE)
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
