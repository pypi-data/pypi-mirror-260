import sys
import socket

def send_sgd_query(ip, port, command):
    response = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(command.encode())
            s.shutdown(socket.SHUT_WR)
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data.decode()
    except Exception as e:
        print(f"Error sending command: {e}")
    return response.strip()

# Replace with your printer's IP address
printer_ip = sys.argv[1]
printer_port = 9100

# SGD commands to get IP and HTTP port
ip_command = "! U1 getvar \"ip.addr\"\r\n"
port_command = "! U1 getvar \"ip.port\"\r\n"

# Sending commands and receiving responses
ip_address = send_sgd_query(printer_ip, printer_port, ip_command)
http_port = send_sgd_query(printer_ip, printer_port, port_command)

print(f"Printer IP Address: {ip_address}")
print(f"HTTP Port: {http_port}")
