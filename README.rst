wnotify
=======

WeeChat remote notification.

On server
---------

Hint: This python script is WeeChat plugin and server at the same time.

On the server where WeeChat is running open shell and do::

  $ cd ~/.weechat/python/autoload
  $ wget https://raw.github.com/matej64/wnotify/master/wnotify-server.py

Inside WeeChat run this command::
  
  /python autoload

Go back to shell and run::

  $ python ~/.weechat/python/autoload/wnotify-server.py &

To make sure that python scripts run on server every time you boot it, run this command in shell as user::
  
  $ crontab -e

Add this line at the end::
  
  @reboot /full/path/python /home/username/.weechat/python/autoload/wnotify-server.py

Save and close it.

Hint: At ubuntu/debian/mint you can find **/full/path/python** with::

  $ which python

 
On client
---------

To connect to server from your client(needed to be done just once)::

  $ cd
  $ wget https://raw.github.com/matej64/wnotify/master/wnotify-client.py
  $ ssh user@server.xyz -L 23567:localhost:23567 2> ~/.ssh-errors.log
  $ python ~/wnotify-client.py &

Hint: ssh command run everytime you want to have see notifications and see WeeChat 

To make sure that python scripts run on client every time you boot it, run this command in shell as user::
  
  $ crontab -e

Add this line at the end::
  
  @reboot /full/path/python /home/username/wnotify-client.py

Save and close it.

Hint: to understand **-L 23567:localhost:23567** look **man ssh**

Hint: we added **2> ~/.ssh-errors.log** to pipe stderr to file 

That it! When you see notification on screen you can switch to terminal window where
is WeeChat running and read the rest.
