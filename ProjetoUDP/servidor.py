import socket 
from threading import Thread

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('',12000))

def loop():
    while True:
        msgBytes, endCliente = servidor.recvfrom(2048) 
        msgBytes = msgBytes.decode()
        print(msgBytes, endCliente)
        #servidor.sendto(msgBytes.encode(), endCliente)

Thread(target=loop).start()




