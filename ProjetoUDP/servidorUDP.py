from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import random
import time

servidor_socket = socket(AF_INET, SOCK_DGRAM)
servidor_socket.bind(("localhost",9500))

def lerArquivo(arquivo):
    perguntas = []
    lista = []
    cont = 0
    for linha in arquivo:
        linha = linha.strip()
        if cont <= 1:
            lista.append(linha)
            cont += 1
        else:
            perguntas.append(lista)
            lista = []
            cont = 0
            lista.append(linha)
            cont += 1
    perguntas.append(lista)        
    return perguntas

def receber_dados():

    while True:
        dados, cliente_endereco = servidor_socket.recvfrom(2048)    
        dados = dados.decode()
        print(dados)
        print(cliente_endereco)

while True:
    Thread(target=receber_dados).start()




arquivo = open("campeoes.txt", "r")
perguntas = lerArquivo(arquivo)
arquivo.close()

