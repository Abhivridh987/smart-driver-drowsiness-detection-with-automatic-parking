import socket

ESP_32_IP = '192.168.5.9' # Provide the IP addreess of your ESP 32 device here
PORT = 12345 # Change this to the port number you want to use

while True:
    message = input('Enter the message to send to ESP32 or type "exit" to quit: ')
    
    if message.lower() == 'exit':
        break

    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to ESP32 Device
        sock.connect((ESP_32_IP, PORT))
        
        # Send the message
        sock.send(message.encode())
        
        response = sock.recv(1024).decode()
        print(f'Response from ESP32: {response}')
    except Exception as e:
        print(f'Error: {e}')
    