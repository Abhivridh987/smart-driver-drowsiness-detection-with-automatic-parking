import socket

ESP_32_IP = "192.168.4.1"
PORT = 5000

class Sender():
    def __init__(self, esp_ip, port):
        self.esp_ip = esp_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.sock.connect((self.esp_ip, self.port))
    
    def close(self):
        self.sock.close()

    def send(self,message):
        self.sock.sendall((message + "\n").encode("utf-8"))
    
    def response(self):
        return self.sock.recv(1024).decode("utf-8")
    

sender = Sender(ESP_32_IP, PORT)

try:
    sender.connect()
    print("Connected to ESP32")

    while True:
        message = input('Enter message or type "exit" to quit: ')

        if message.lower() == "exit":
            break

        sender.send(message)

        response = sender.response()
        print(f"Response from ESP32: {response}")
        
except Exception as e:
    print(f"An error occurred: \n{e}")

finally:
    sender.close()
    print("Connection closed")