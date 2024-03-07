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

# Replace with your printer's IP address
printer_ip = "192.168.1.29"  
printer_port = 9100

# SGD command to clear the WML file setting
clear_wml_file_command = "! U1 setvar \"wml.file\" \"XXX\"\r\n"

# Sending the command
send_sgd_command(printer_ip, printer_port, clear_wml_file_command)
