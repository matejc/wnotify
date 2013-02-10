wnotify
=======

WeeChat remote notification.


On server
---------

Dependency: openssl

Connect to machine where your *weechat* is running and then::

  $ cd ~/.weechat/python/
  $ git clone git://github.com/matejc/wnotify.git
  $ cd wnotify


Create certificate for SSL connection::

  $ openssl genrsa -des3 -out server.key 4096
  $ openssl rsa -in server.key -out server.key.insecure
  $ mv server.key server.key.secure
  $ mv server.key.insecure server.key
  $ openssl req -new -key server.key -out server.csr
  $ openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt


Configuration (change at least *password* field AND bind *address*)::

  $ cp wnserver.conf.example wnserver.conf
  $ nano wnserver.conf


Link the *wnotify-server.py* to the autoload directory::

  $ ln -s ~/.weechat/python/wnotify/wnotify-server.py ~/.weechat/python/autoload/


Activate weechat plugin, run this command inside weechat::

  /python autoload


Go back to shell and run to start the server::

  $ python ~/.weechat/python/wnotify/wnotify-server.py &


To make sure that python scripts run on server every time you boot it,
run this command in shell as user::
  
  $ crontab -e


Add this line at the end::
  
  @reboot /full/path/python /home/username/.weechat/python/wnotify-server.py


Save and close it.

Hint: You can find **/full/path/python** with::

  $ which python


On client
---------

Dependency: Tk (for notification window)

Connect to machine where you want to notifications to be visible::

  $ cd ~/some/path/
  $ git clone git://github.com/matejc/wnotify.git
  $ cd wnotify


Configuration (change *address* to servers ip or domain AND *password* to match servers)::

  $ cp wnserver.conf.example wnserver.conf
  $ nano wnserver.conf


Run::

  $ python ~/some/path/wnotify/wnotify-client.py


Run this command at every boot, by adding it to autostart in your desktop/window manager settings.


That it! When you see notification on screen you can switch to terminal window where
is WeeChat running and read the rest.
