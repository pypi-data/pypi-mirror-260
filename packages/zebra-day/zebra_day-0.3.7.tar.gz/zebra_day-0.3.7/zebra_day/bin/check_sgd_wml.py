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
printer_ip = "192.168.1.29"
printer_port = 9100

# SGD commands to get the expected WML file and check if it exists
expected_wml_file_command = "! U1 getvar \"display.root_wml\"\r\n"
file_exists_command = lambda filename: f"! U1 do \"file.type\" \"{filename}\"\r\n"

# Sending commands and receiving responses
expected_wml_file = send_sgd_query(printer_ip, printer_port, expected_wml_file_command)
file_exists_response = send_sgd_query(printer_ip, printer_port, file_exists_command(expected_wml_file))

print(f"Expected WML File: {expected_wml_file}")
print(f"File Exists Response: {file_exists_response}")
