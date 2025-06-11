import os
import socket
import threading
import json
import subprocess
import signal
import sys

SOCKET_PATH = "/tmp/timer_daemon.sock"
timers = {}  # Dictionary to store timers: {name: (timer, timeout, command)}

def execute_command(command):
    """Execute the command in a subprocess."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")

def timer_callback(name, command):
    """Callback when a timer expires."""
    print(f"Timer '{name}' expired, executing: {command}")
    execute_command(command)
    if name in timers:
        del timers[name]  # Remove timer after execution

def handle_client(conn):
    """Handle incoming client connections."""
    try:
        data = conn.recv(1024).decode()
        if not data:
            return
        request = json.loads(data)
        command = request.get("command")
        response = {"status": "success", "message": ""}

        if command == "add":
            name = request.get("name")
            timeout = float(request.get("timeout"))
            cmd = request.get("cmd")
            if name in timers:
                response = {"status": "error", "message": f"Timer '{name}' already exists"}
            else:
                timer = threading.Timer(timeout, timer_callback, args=(name, cmd))
                timer.start()
                timers[name] = (timer, timeout, cmd)
                response["message"] = f"Timer '{name}' added with timeout {timeout}s"

        elif command == "delete":
            name = request.get("name")
            if name in timers:
                timer, _, _ = timers[name]
                timer.cancel()
                del timers[name]
                response["message"] = f"Timer '{name}' deleted"
            else:
                response = {"status": "error", "message": f"Timer '{name}' not found"}

        elif command == "ls":
            timer_list = [{"name": name, "timeout": timeout, "command": cmd}
                          for name, (_, timeout, cmd) in timers.items()]
            response["timers"] = timer_list

        elif command == "set":
            name = request.get("name")
            new_timeout = float(request.get("new_timeout"))
            if name in timers:
                timer, _, cmd = timers[name]
                timer.cancel()  # Cancel the old timer
                new_timer = threading.Timer(new_timeout, timer_callback, args=(name, cmd))
                new_timer.start()
                timers[name] = (new_timer, new_timeout, cmd)
                response["message"] = f"Timer '{name}' timeout updated to {new_timeout}s"
            else:
                response = {"status": "error", "message": f"Timer '{name}' not found"}

        else:
            response = {"status": "error", "message": "Invalid command"}

        conn.send(json.dumps(response).encode())
    except Exception as e:
        conn.send(json.dumps({"status": "error", "message": str(e)}).encode())
    finally:
        conn.close()

def start_server():
    """Start the Unix socket server."""
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)
    
    print("Timer daemon started, listening on", SOCKET_PATH)
    
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def cleanup(signum, frame):
    """Cleanup on termination."""
    for name, (timer, _, _) in timers.items():
        timer.cancel()
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    start_server()