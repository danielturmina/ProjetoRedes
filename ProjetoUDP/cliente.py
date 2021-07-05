from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time

encerra = False
cliente = socket(AF_INET, SOCK_DGRAM)

print('digite seu nome:\n') #aparece só uma vez assim que inicia o cliente

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
msg = 'Conectado: '# manda uma msg automatica assim que inicia o servidor, para que o servidor entendenda que esse usuario conectou
cliente.sendto(msg.encode(),('localhost',12000))

Thread(target=recebe).start()
Thread(target=envia).start()

