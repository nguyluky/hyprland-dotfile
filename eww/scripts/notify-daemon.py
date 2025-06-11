import json
import os
import socket
import threading
import subprocess
import dbus
import dbus.service
import logging
from logging.handlers import RotatingFileHandler
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

# Create log directory if it doesn't exist
LOG_DIR = os.path.expanduser('~/.config/eww/logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            f'{LOG_DIR}/notification-daemon.log', 
            maxBytes=1024*1024*5,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger("eww-notification-daemon")

# Replace FIFO with Unix socket
SOCKET_PATH = '/tmp/eww-notifications.sock'
# Remove socket if it already exists
if os.path.exists(SOCKET_PATH):
    os.unlink(SOCKET_PATH)

# Create and setup socket server
server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_socket.bind(SOCKET_PATH)
server_socket.listen(5)
# Set socket permissions
os.chmod(SOCKET_PATH, 0o777)

# List to keep track of client connections
clients = []

def socket_server_thread():
    """Background thread to handle incoming socket connections"""
    while True:
        try:
            client, _ = server_socket.accept()
            clients.append(client)
            logger.info(f"New client connected. Total clients: {len(clients)}")
        except Exception as e:
            logger.error(f"Socket accept error: {e}")
            break

# Start socket server in background thread
socket_thread = threading.Thread(target=socket_server_thread, daemon=True)
socket_thread.start()

logger.info("Socket server started")

def send_to_clients(data):
    """Send data to all connected clients"""
    # Convert notification data to array format
    arr = []
    for key, value in data.items():
        notification_id = key
        app_name = value['app_name']
        app_icon = value['app_icon']
        summary = value['summary']
        body = value['body']
        actions = value['actions']
        hints = value['hints']
        expire_timeout = value.get('expire_timeout', -1)  # Default -1 if not present

        notification_data = {
            'id': notification_id,
            'app_name': app_name,
            'app_icon': app_icon.replace('file://', ''),
            'summary': summary,
            'body': body,
            'actions': [{'id': actions[i], 'label': actions[i+1]} for i in range(0, len(actions), 2)],
            'hints': {str(k): str(v) for k, v in hints.items()},
            'expire_timeout': expire_timeout
        }
        arr.append(notification_data)
    
    # Convert to JSON and add newline
    json_data = json.dumps(arr) + '\n'
    json_bytes = json_data.encode('utf-8')
    
    # Send to all connected clients
    disconnected_clients = []
    for client in clients:
        try:
            client.sendall(json_bytes)
        except (BrokenPipeError, ConnectionResetError) as e:
            logger.warning(f"Client disconnected: {e}")
            disconnected_clients.append(client)
            
    # Clean up disconnected clients
    for client in disconnected_clients:
        clients.remove(client)
        try:
            client.close()
        except:
            pass
            
    logger.info(f"Sent data to {len(clients)} clients: {arr}")

class NotificationService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName("org.freedesktop.Notifications", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/org/freedesktop/Notifications")
        self.next_id = 1
        self.notifications = {}  # Lưu thông tin thông báo
        self.timers = {}  # Lưu các bộ hẹn giờ

    @dbus.service.method("org.freedesktop.Notifications", 
                         in_signature='susssasa{sv}i', 
                         out_signature='u')
    def Notify(self, app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout):
        notification_id = replaces_id if replaces_id > 0 else self.next_id
        if replaces_id == 0:
            self.next_id += 1
            
        # Hủy bộ hẹn giờ cũ nếu tồn tại (cho trường hợp thay thế notification)
        if notification_id in self.timers:
            GLib.source_remove(self.timers[notification_id])
            del self.timers[notification_id]
        
        # Lưu thông tin thông báo để xử lý sau này
        self.notifications[notification_id] = {
            'app_name': app_name,
            'app_icon': app_icon,
            'summary': summary,
            'body': body,
            'actions': actions,
            'hints': hints,
            'expire_timeout': expire_timeout
        }


        send_to_clients(self.notifications)

        # logger.info("data: \n%s", str(self.notifications))
        
        logger.info(f"{'Field':<15} | {'Value'}")
        logger.info(f"{'-'*15}-|-{'-'*30}")
        logger.info(f"{'Notification ID':<15} | {notification_id}")
        logger.info(f"{'App Name':<15} | {app_name}")
        logger.info(f"{'App Icon':<15} | {app_icon}")
        logger.info(f"{'Summary':<15} | {summary}")
        logger.info(f"{'Actions':<15} | {actions}")
        logger.info(f"{'Expire Timeout':<15} | {expire_timeout}")
        logger.info(f"{'Hints':<15} | {hints}")
        
        # Bắn sự kiện để UI cập nhật
        self.NotificationReceived(notification_id, app_name, app_icon, summary, body)
        
        # Thiết lập bộ hẹn giờ để tự động xóa thông báo nếu expire_timeout > 0
        if expire_timeout > 0:
            # expire_timeout đơn vị là milliseconds
            self.timers[notification_id] = GLib.timeout_add(
                expire_timeout, 
                self._expire_notification, 
                notification_id
            )
        elif expire_timeout == -1:
            # Sử dụng thời gian mặc định nếu expire_timeout = -1
            default_timeout = 5000  # 5 giây
            self.timers[notification_id] = GLib.timeout_add(
                default_timeout,
                self._expire_notification,
                notification_id
            )
        
        return notification_id
    
    def _expire_notification(self, notification_id):
        """Hàm được gọi khi thông báo hết hạn"""
        logger.info(f"Notification {notification_id} expired")
        
        # Xóa thông báo khỏi cache
        if notification_id in self.notifications:
            del self.notifications[notification_id]
        
        # Xóa timer
        if notification_id in self.timers:
            del self.timers[notification_id]
        
        # Gửi signal NotificationClosed với reason=1 (timeout)
        self.NotificationClosed(notification_id, 1)
        
        return False  # Trả về False để GLib không tiếp tục gọi hàm này
    
    @dbus.service.method("org.freedesktop.Notifications", 
                         in_signature='', 
                         out_signature='as')
    def GetCapabilities(self):
        # Thêm các capability để hỗ trợ tương tác
        return ["actions", "body", "body-markup", "action-icons", "persistence"]
                
    @dbus.service.signal("org.freedesktop.Notifications", signature='uu')
    def NotificationClosed(self, notification_id, reason):
        """
        Handles the event when a notification is closed.
        Args:
            notification_id (int): The unique identifier of the notification that was closed.
            reason (int): The reason why the notification was closed. Possible values:
                - 1: Expired
                - 2: Dismissed by the user
                - 3: Closed by a call to the CloseNotification method
                - 4: Undefined reason
        Behavior:
            - Removes the notification from the cache if it exists.
            - Cancels and removes the associated timer if it exists.
            - Updates the FIFO (First In, First Out) mechanism with the current notifications.
        """
        logger.info(f"Notification {notification_id} closed with reason {reason}")
        # Xóa thông báo khỏi cache khi đóng
        if notification_id in self.notifications:
            del self.notifications[notification_id]
            
        # Hủy bộ hẹn giờ nếu tồn tại
        if notification_id in self.timers:
            GLib.source_remove(self.timers[notification_id])
            del self.timers[notification_id]
        
        send_to_clients(self.notifications)
        pass
    
    @dbus.service.method("org.freedesktop.Notifications", 
                         in_signature='u', 
                         out_signature='')
    def CloseNotification(self, notification_id):
        """Phương thức đóng thông báo theo spec Freedesktop"""
        # Gửi signal NotificationClosed với reason=3 (close_notification)
        self.NotificationClosed(notification_id, 3)
    
    @dbus.service.method("org.freedesktop.Notifications", 
                         in_signature='', 
                         out_signature='ssss')
    def GetServerInformation(self):
        return ("EWW Notification Server", "EWW", "1.0", "1.2")
    
    # # Thêm phương thức xử lý việc nhấn vào thông báo
    @dbus.service.method("org.freedesktop.Notifications",
                        in_signature='us',
                        out_signature='')
    def InvokeAction(self, notification_id, action_key):
        self.ActionInvoked(notification_id, action_key)
        # self._connection : dbus.connection.Connection
        
    #     return (notification_id, action_key)
    
    # Thêm phương thức để mở ứng dụng khi người dùng nhấn vào thông báo
    def _handle_default_action(self, notification):
        app_name = notification['app_name']
        hints = notification['hints']
        
        logger.info(f"Handling default action for app: {app_name}")

        # Kiểm tra xem có URL trong hints không
        if 'x-kde-urls' in hints:
            urls = hints['x-kde-urls']
            subprocess.Popen(['xdg-open', urls])
            return


        # hyprland forcus to this app
        # Nếu không có URL, kiểm tra xem có desktop entry không
        # if 'desktop-entry' in hints:
        #     desktop_entry = hints['desktop-entry']

        #     logger.info(f"Opening application with desktop entry: {desktop_entry}")
        #     subprocess.Popen(['gtk-launch', desktop_entry])
        #     return
    
    @dbus.service.signal("org.freedesktop.Notifications", signature="us")
    def ActionInvoked(self, id, action_key):
        
        """
        Handles the event when an action is invoked on a notification.
        Args:
            id (int): The unique identifier of the notification.
            action_key (str): The action that was invoked.
        Behavior:
            - Prints the notification ID and action to the console.
            - Calls the _handle_default_action method to perform the default action associated with the notification.
        """
        logger.info(f"Action invoked: {id}, action: {action_key}")
        if action_key == "default":
            self._handle_default_action(self.notifications.get(id, {}))
        pass
        
    # Signal khi nhận thông báo mới (để UI cập nhật)
    @dbus.service.signal("org.freedesktop.Notifications", signature='ussss')
    def NotificationReceived(self, notification_id, app_name, app_icon, summary, body):
        pass

if __name__ == "__main__":
    
    # Initialize the DBus main loop
    DBusGMainLoop(set_as_default=True)
    
    # Create and initialize the notification service
    notification_service = NotificationService()
    
    logger.info("EWW Notification Daemon started")
    
    # Start the main loop
    mainloop = GLib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        logger.info("Notification daemon stopped")