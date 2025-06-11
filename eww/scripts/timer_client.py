import sys
import socket
import json

SOCKET_PATH = "/tmp/timer_daemon.sock"

def send_command(command_data):
    """Send command to the daemon and return the response."""
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(SOCKET_PATH)
        client.send(json.dumps(command_data).encode())
        response = json.loads(client.recv(1024).decode())
        return response
    except Exception as e:
        return {"status": "error", "message": f"Failed to communicate with daemon: {e}"}
    finally:
        client.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: timer_client.py <command> [args]")
        print("Commands: add <name> <timeout> <command>, delete <name>, ls, set <name> <new_timeout>")
        sys.exit(1)

    command = sys.argv[1].lower()
    response = None

    if command == "add" and len(sys.argv) >= 5:
        name, timeout, cmd = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
        response = send_command({"command": "add", "name": name, "timeout": timeout, "cmd": cmd})
    elif command == "delete" and len(sys.argv) == 3:
        name = sys.argv[2]
        response = send_command({"command": "delete", "name": name})
    elif command == "ls" and len(sys.argv) == 2:
        response = send_command({"command": "ls"})
    elif command == "set" and len(sys.argv) == 4:
        name, new_timeout = sys.argv[2], sys.argv[3]
        response = send_command({"command": "set", "name": name, "new_timeout": new_timeout})
    else:
        print("Invalid command or arguments")
        print("Commands: add <name> <timeout> <command>, delete <name>, ls, set <name> <new_timeout>")
        sys.exit(1)

    if response["status"] == "error":
        print(f"Error: {response['message']}")
    else:
        if command == "ls":
            if response.get("timers"):
                for timer in response["timers"]:
                    print(f"Name: {timer['name']}, Timeout: {timer['timeout']}s, Command: {timer['command']}")
            else:
                print("No timers found")
        else:
            print(response["message"])

if __name__ == "__main__":
    main()