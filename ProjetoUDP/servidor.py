import socket 
from threading import Thread
import random

#variaveis
jogadores = []



#cria servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('',12000))
####

#trata o banco de dados em txt
def lerArquivo(arquivo):
    perguntas = []
    lista = []
    cont = 0
    for linha in arquivo:
        linha = linha.strip()
        lista.append(linha)
    while cont+1 <= len(lista):
        tupla = (lista[cont],lista[cont+1])
        perguntas.append(tupla)
        cont += 2      
    return perguntas


arquivo = open('C:\\Users\\YNC\\Documents\\codigosEstudos\\campeoes.txt', "r")  
perguntas = lerArquivo(arquivo)
arquivo.close()
#####


perguntaSortida = [] #lista com 5 tuplas de perguntas e respostas

sorteio = random.sample(range(0,19), 5) #sorteia uma lista com 5 numero sem repetições *mais eficaz
for i in sorteio: #add 5 tuplas de perguntas e respostas a uma lista
    perguntaSortida.append(perguntas[int(i)]) 

print(perguntaSortida) #verificando se deu certo
input('') #debugando


def enviaTodos(lista, msg): #envia msg a todos
    for i in lista:
        servidor.sendto(msg.encode().upper(), i)

def loop():
    while True:
        msgBytes, endCliente = servidor.recvfrom(2048) 
        msgBytes = msgBytes.decode()
        if endCliente not in jogadores:
            jogadores.append(endCliente)
        print(msgBytes, endCliente) #debugando
        enviaTodos(jogadores, msgBytes)
        #servidor.sendto(msgBytes.encode(), endCliente)
        #print('mandou')

Thread(target=loop).start()




