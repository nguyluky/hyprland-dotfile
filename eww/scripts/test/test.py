
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def handle_action_invoked(nid, action_key):
    print(f"Action Invoked: {action_key} on notification {nid}")

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

bus.add_signal_receiver(
    handle_action_invoked,
    dbus_interface="org.freedesktop.Notifications",
    signal_name="ActionInvoked"
)

notify_obj = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
notify = dbus.Interface(notify_obj, 'org.freedesktop.Notifications')

actions = ["open", "Open", "close", "Close", 'default', 'Default']
notify.Notify("MyApp", 0, "", "Title", "Choose an action", actions, {}, -1)

loop = GLib.MainLoop()
loop.run()
