import dbus
import time

bus = dbus.SessionBus()
notify_object = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
notify_interface = dbus.Interface(notify_object, "org.freedesktop.Notifications")

app_name = "ProgressApp"
replaces_id = 0  # để cập nhật thông báo sau này
icon = ""
summary = "Đang xử lý"
body = "Tiến trình: 0%"
actions = []
hints = {
    'value': dbus.Int32(0)  # đây là phần chính tạo thanh tiến trình!
}
expire_timeout = 1000  # milliseconds

# Gửi thông báo ban đầu
replaces_id = notify_interface.Notify(app_name, replaces_id, icon, summary, body, actions, hints, expire_timeout)

# Cập nhật tiến trình
for i in range(1, 101):
    body = f"Tiến trình: {i}%"
    hints['value'] = dbus.Int32(i)
    replaces_id = notify_interface.Notify(app_name, replaces_id, icon, summary, body, actions, hints, expire_timeout)
    time.sleep(1)
