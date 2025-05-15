import socket

client = socket.socket()
client.connect(('622a-177-126-81-235.ngrok-free.app', 8080))

print("[CLIENTE] Conectado ao servidor")

# Simula uma requisição recebida no servidor
while True:
    data = input("Digite algo para enviar ao servidor: ")
    client.send(data.encode())
