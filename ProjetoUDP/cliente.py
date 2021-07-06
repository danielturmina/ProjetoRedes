from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

encerra = False
cliente = socket(AF_INET, SOCK_DGRAM)


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


texto = 'Conectado: '
while True: # Pedindo nome e evitando nomes vazios
    nome = input('Digite o seu nome: \n')
    if len(nome) > 0:
        break 
msg = texto + nome
cliente.sendto(msg.encode(),('localhost',12000))
 

Thread(target=recebe).start()
Thread(target=envia).start()
