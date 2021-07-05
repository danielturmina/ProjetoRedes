from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

encerra = False
cliente = socket(AF_INET, SOCK_DGRAM)

print('digite seu nome:\n')

def envia():
    global encerra
    while True:
        if encerra:
            break
        msg = input('')
        cliente.sendto(msg.encode(),('localhost',12000))

def recebe():
    while True:
        msgBytes, endServidor = cliente.recvfrom(2048)
        print(msgBytes.decode())

#é preciso ter esse inicio pra o servidor se conectar com cliente primeiramente
msg = 'Conectado: '#input('nome do jogador\n') 
cliente.sendto(msg.encode(),('localhost',12000))
#################

Thread(target=recebe).start()
Thread(target=envia).start()

