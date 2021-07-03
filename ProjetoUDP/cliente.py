import socket
import threading
import time

encerra = False 
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def envia():
    global encerra #talvez usar POO futuramente
    while True:
        if encerra:
            break
        msg = input('digite a msg')
        cliente.sendto(msg.encode(),('localhost',12000))

def recebe():
    while True:
        msgBytes, endServidor = cliente.recvfrom(2048)
        print(msgBytes.decode())

#eh preciso ter esse inicio pra o servidor se conectar com o cliente primeiramente
msg = input('nome do jogador\n') 
cliente.sendto(msg.encode(),('localhost',12000))
#################

threading.Thread(target=recebe).start()
threading.Thread(target=envia).start()

