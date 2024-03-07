import socket

def send_sgd_command(ip, port, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(command.encode())
            s.shutdown(socket.SHUT_WR)
            print(f"Command sent: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

# Replace with your printer's current IP address
printer_ip = "192.168.1.29"  
printer_port = 9100

# Replace with your desired static IP, subnet mask, and gateway
new_ip = "192.168.1.29"
subnet_mask = "255.255.255.0"
gateway = "192.168.1.1"

# SGD commands to set IP, subnet, gateway, and HTTP port
commands = [
    f"! U1 setvar \"ip.addr\" \"{new_ip}\"\r\n",
    f"! U1 setvar \"ip.mask\" \"{subnet_mask}\"\r\n",
    f"! U1 setvar \"ip.gateway\" \"{gateway}\"\r\n",
    "! U1 setvar \"ip.port\" \"80\"\r\n",
    "! U1 setvar \"web.enable\" \"true\"\r\n"
]

# Sending commands
for cmd in commands:
    send_sgd_command(printer_ip, printer_port, cmd)
