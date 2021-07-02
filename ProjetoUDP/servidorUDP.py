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
        lista.append(linha)
    while cont+1 <= len(lista):
        tupla = (lista[cont],lista[cont+1])
        perguntas.append(tupla)
        cont += 2      
    return perguntas

def enviar_dados(msg, cliente_endereco):
    servidor_socket.sendto(msg.encode(),cliente_endereco)

def iniciarPartida():
    global comecou
    comecou = True
    rodada = []
    while len(rodada) < 5:
        escolher = random.choice(perguntas)
        rodada.append(escolher)
    print(rodada)
    

def receber_dados():
    while True:
        dados, cliente_endereco = servidor_socket.recvfrom(2048)    
        dados = dados.decode()
        print(f"Servidor recebeu: {dados} do cliente: {cliente_endereco}")
        if len(listaJogadores) < 5 and cliente_endereco not in listaClientes and comecou == False:
            listaJogadores.append([dados,cliente_endereco])
            listaClientes.append(cliente_endereco)
            enviar_dados("Digite 'start' para começar",cliente_endereco)
            print(listaPontuacao)
            print(listaJogadores)
        elif cliente_endereco not in listaClientes and comecou == True:
            enviar_dados("Você não poderá participar do Jogo pois a Partida já começou! Jogo Encerrado!",cliente_endereco)
        elif cliente_endereco not in listaClientes and len(listaJogadores) >= 5:
            enviar_dados("Você não poderá participar do Jogo pois já atingimos o limite de Participantes! Jogo Encerrado!",cliente_endereco)
        elif dados == "start"and cliente_endereco not in preparados:
            if comecou == False:
                preparados.append(cliente_endereco)
                listaPontuacao.append([cliente_endereco,0])
                enviar_dados("A partida iniciará em breve!",cliente_endereco)
                if len(preparados)>=2:
                    time.sleep(30)
                    iniciarPartida()
            else:
                enviar_dados("Você não deu start a tempo, a partida já começou",cliente_endereco)

         
listaJogadores = []
listaClientes = []
listaPontuacao = []
qnt = 0
preparados = []
comecou = False

arquivo = open("campeoes.txt", "r")
perguntas = lerArquivo(arquivo)
arquivo.close()

while True:
    Thread(target=receber_dados).start()
