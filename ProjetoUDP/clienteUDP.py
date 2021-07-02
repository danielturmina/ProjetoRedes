from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

sock = socket(AF_INET, SOCK_DGRAM)



def enviarDados(msg):
    sock.sendto(msg.encode(), ("localhost",9500))

def receber_dados(sock):
        while True:
            dados = sock.recv(2048)
            print(f"{dados.decode()}")
            if dados == "Você não poderá participar do Jogo pois a Partida já começou!":
                sock.close()
            elif dados == "Você não poderá participar do Jogo pois já atingimos o limite de Participantes!":
                sock.close()
            elif dados == "Você não deu start a tempo, a partida já começou":
                sock.close()
            else:
                responder = input()
                enviarDados(responder)

print("Seja Bem Vindo - Quiz Copa do Mundo")
nome = ""

while len(nome) < 1 :
    nome = input("\nDigite seu Nome:")

enviarDados(nome)

Thread(target = receber_dados, args=(sock,)).start()

