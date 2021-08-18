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

def clienteInicio():
    print("--- Quiz: Campeões do Mundo! --- \nAperte Enter para Continuar\n")
    texto = 'Conectado: '
    while True: 
        nome = input('Digite seu nome:\n') 
        if len(nome) > 0:
            break 
    msg = texto + nome
    cliente.sendto(msg.encode(),('localhost',12000))

def recebe():
    while True:
        msgBytes, endServidor = cliente.recvfrom(2048)
        if msgBytes.decode() in dicRespostas:
            texto = msgBytes.decode()
            print(dicRespostas[texto])
        else: 
            print(msgBytes.decode())
        
        if msgBytes.decode() == '600':
            clienteInicio()

print("--- Quiz: Campeões do Mundo! --- ")
texto = 'Conectado: '
while True:
    nome = input('Digite seu nome:') 
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
'300':'Você errou! Tente novamente...',
'400': 'Uma nova partida está para começar\nDeseja iniciar? [s/n]\n',
'500': 'Ok aguarde o inicio do jogo!',
'501': 'Tudo bem, obrigado por participar, até logo!',
'502': 'Aguarde até que o jogo reinicie!',
'600': 'A partida irá reiniciar em instantes'}

Thread(target=recebe).start()
Thread(target=envia).start()
