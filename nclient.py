import socket
import time
import os


ADDRESS = "localhost"
PORT = 23567
PASSWORD = "er98vzt2945z42zt8j798z7TZ=/(Tn675ev5v6584553W$47e9876Tvl3py7"



prev_data = ""

def onecycle():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDRESS, PORT))

    s.settimeout(5)
    
    s.sendall( PASSWORD )
    
    return_data = s.recv(1024)
    s.close()

    global prev_data
    if return_data != prev_data:
        os.system("notify-send WeeChat \"%s\"" % return_data)
        prev_data = return_data



try:
    
    while True:
        try:
            onecycle()
        except:
            pass
        time.sleep(10)

except KeyboardInterrupt:
    print "\nUser killed the program!"

finally:
    print "Client killed!"
