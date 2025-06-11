import os
import socket
import json
import time
import logging
from logging.handlers import RotatingFileHandler
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

theme = Gtk.IconTheme.get_default()

# Configure logging
LOG_DIR = os.path.expanduser('~/.config/eww/logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            f'{LOG_DIR}/notification-client.log', 
            maxBytes=1024*1024*5,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger("eww-notification-client")

# Unix socket path
SOCKET_PATH = '/tmp/eww-notifications.sock'

close_notification = lambda notification_id: f"gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.CloseNotification \
  {notification_id}"

invoke_action = lambda notification_id, action: f"gdbus call --session \
  --dest org.freedesktop.Notifications \
  --object-path /org/freedesktop/Notifications \
  --method org.freedesktop.Notifications.InvokeAction \
  {notification_id} '{action}'"

def make_img(url):
    if url == '':
        return ''

    if '/' not in url:
        info = theme.lookup_icon(url, 64, 0)

        if not info:
            logger.warning(f"Icon '{url}' not found in theme, using default icon.")
            return ''
        url = info.get_filename()

    return f'(image :path "{url}" :class "app-icon" :image-width 30 :image-height 30)'

def make_action_button(notify_id, actions):
    l = []
    for action in actions:
        l.append(f'(button :class "action-button" :height 30 :onclick "{invoke_action(notify_id, action.get("id", "default"))}" "{action.get("label", "Action")}" )')

    return f'''( box :class "notificatios-actions" :spacing 5 {' '.join(l)} )'''

def es(s: str):
    # Escape all double quotes in the string
    return s.replace('"', '\\\"')

def make_yuck(data):
    yuck_str = ''
    
    for notify in data:
        notify_id = notify.get('id', 0)
        app_name = notify.get('app_name', 'Unknown App')
        app_icon = notify.get('app_icon', '')
        summary = notify.get('summary', 'No Summary')
        body = notify.get('body', 'No Body')
        actions = notify.get('actions', [])
        expire_timeout = notify.get('expire_timeout', -1)
        hints = notify.get('hints', {})

        # kiểm tra nếu có default action và settings action
        has_default_action = any(action.get('id') == 'default' for action in actions)
        has_settings_action = any(action.get('id') == 'settings' for action in actions)

        # bỏ qua default action và settings action
        actions = [action for action in actions if action.get('id') not in ['default', 'settings']]

        if not app_icon:
            app_icon = hints.get('image-path', '')

        # Tạo chuỗi Yuck
        yuck_str += f'''

            (box :class "notification-card"
                (eventbox :onclick "{ invoke_action(notify_id, 'default') if has_default_action else '' }"
                    (box :orientation "v" :space-evenly false :spacing 5
                    (box :orientation "h" :class "notification-header" :space-evenly false :spacing 5
                        {make_img(app_icon)}
                        (label :text "{es(app_name)}" :class "app-name" :limit-width 150 :hexpand true :xalign 0)
                        { f'(button :class "settings-button" :onclick "{invoke_action(notify_id, 'settings')}" :height 30 :width 30 "⚙" )' if has_settings_action else '' }
                        (button :class "close-button" :onclick "{close_notification(notify_id)}" :height 30 :width 30 "✖")
                    )
                    
                    ( box :orientation "v" :class "notification-body" :space-evenly false
                        { f'(label :class "notification-title" :halign "start" :text "{es(summary)}")' if summary else '' }
                        { f'(label :justify "left" :wrap true :xalign 0 :yalign 0 :show-truncated false :class "notification-body" :halign "start" :text "{es(body)}")' if body else '' }
                        { f'( progress :value {hints.get("value", 0)} :hexpand true :class "notification-progress")' if 'value' in hints else '' }
                    )

                    {make_action_button(notify_id, actions) if actions else ''}
                        
                    )
                )
            )
            '''

    string = f'''(box :orientation "vertical" :space-evenly false :spacing 10 :class "notifications-container" 
        {yuck_str}
    )'''

    string = string.replace('\n', ' ')
    # loại bỏ khoảng trắng thừa
    string = ' '.join(string.split())
    return string

# Function to connect to the socket with retries
def connect_to_socket(max_retries=5, retry_delay=1):
    retries = 0
    while retries < max_retries:
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(SOCKET_PATH)
            logger.info("Connected to notification daemon socket")
            return client
        except (FileNotFoundError, ConnectionRefusedError) as e:
            retries += 1
            logger.warning(f"Connection attempt {retries}/{max_retries} failed: {e}")
            if retries < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached, could not connect to socket")
                raise
    return None

# Main loop to read from socket
def main():
    buffer = ""
    while True:
        try:
            client = connect_to_socket()
            
            while True:
                data = client.recv(4096).decode('utf-8')
                if not data:
                    logger.warning("Socket connection closed by server")
                    break
                
                # Add received data to buffer
                buffer += data
                
                # Process complete lines in buffer
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        try:
                            # Parse JSON data
                            parsed_data = json.loads(line)
                            # Generate and print Yuck
                            yuck_output = make_yuck(parsed_data)
                            print(yuck_output, flush=True)
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
                        except Exception as e:
                            logger.error(f"Error processing notification: {e}")
                
        except Exception as e:
            logger.error(f"Socket error: {e}")
            time.sleep(2)  # Wait before reconnecting
            
if __name__ == "__main__":
    main()
