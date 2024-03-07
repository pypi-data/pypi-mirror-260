import socket
import sys

printer_ip = sys.argv[1]

def send_sgd_command(ip, port, command):
    try:
        # Creating a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(command.encode())
            s.shutdown(socket.SHUT_WR)
            print(f"Command sent: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

# Printer IP and port (usually 9100 for Zebra printers)

printer_port = 9100

# SGD commands to set display.root_wml to default and delete WMINDEX.WML
commands = [
    "! U1 setvar \"device.restore_defaults\" \"factory\"\r\n",
    "! U1 setvar \"web.enable\" \"true\"\r\n",
    "! U1 setvar \"ip.port\" \"80\"\r\n"
]

# Sending commands
for cmd in commands:
    send_sgd_command(printer_ip, printer_port, cmd)
