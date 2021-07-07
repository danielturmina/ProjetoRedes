from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time #Não estamos usando

encerra = False # Qual o uso?
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
        if msgBytes.decode() in dicRespostas:
            texto = msgBytes.decode()
            print(dicRespostas[texto])
        else: 
            print(msgBytes.decode())

print("--- Quiz: Campeões do Mundo! --- ")
texto = 'Conectado: '
while True: # Pedindo nome e evitando nomes vazios
    nome = input('Digite o seu nome: \n')
    if len(nome) > 0:
        break 
msg = texto + nome
cliente.sendto(msg.encode(),('localhost',12000))
dicRespostas = {
'100':'Digite "start" para começar:',
'101':'Sua partida está prestes a começar\n',
'102':'A quantidade limite de jogadores foi atingida! Tente novamente mais tarde!\n',
'103':'Infelizmente você não digitou "start" a tempo, a partida já iniciou!\n',
'104':'Partida já iniciada, volte mais tarde!!\n',
'200':'Você acertou!',
'300':'Você errou! Tente novamente...'}


Thread(target=recebe).start()
Thread(target=envia).start()
