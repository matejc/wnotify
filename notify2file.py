import weechat
import os

weechat.register('notify2file', '', '1.0', 'GPL', 'WeeChat script for writing notification messages to file.', '', '')

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
    notifyfile.write(message)
    notifyfile.write("\n")
    notifyfile.close()
