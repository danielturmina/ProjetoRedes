'''Cada rodada será encerrada quando algum participante acertar a resposta ou atingir
uma duração máxima de 10 segundos;
Pontuação de cada rodada: Cada resposta errada: -5 pontos, sem resposta: -1 ponto, Resposta correta: 25 pontos
Após uma competição ser encerrada, um ranking com a pontuação é divulgado e uma nova competição poderá ser iniciada.'''

import socket 
from threading import Thread
import random
import time

#testar futuramente
class Jogadores:
    def __init__(self):
        self.pronto = False
        self.nome = ''
        self.pontos = 0
        self.end = ''

jogadores = []
jogadoresProntos = []
perguntaSortida = [] 
comecou = False
start = True
numRodada = 0
porta = 12000
contTempo = 10 #usei dez segundos pra o criterio q o prof pede, além disso é usado tanto pra iniciar um jogo quanto pra tempo de resposta
tempoInterrompido = False

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('', porta)) 

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

arquivo = open('campeoes.txt', "r") 
perguntas = lerArquivo(arquivo)
arquivo.close()

sorteio = random.sample(range(0,19), 5) 
for i in sorteio: 
    perguntaSortida.append(perguntas[int(i)]) 

print(perguntaSortida) #debug

def enviaTodos(lista, msg): #envia msg a todos
    for i in lista:
        servidor.sendto(msg.encode(), i)

def recebe():
    msgRecebida, endRecebido = servidor.recvfrom(2048) 
    msgRecebida = msgRecebida.decode()
    return [msgRecebida, endRecebido]

def cronometro():
    
    global contTempo, porta, comecou, tempoInterrompido
    contTempo = 10 
    somaCont = 0

    while contTempo > 0:
        time.sleep(1)
        print(contTempo)
        if not comecou:
            enviaTodos(jogadoresProntos, str(contTempo))
        somaCont += contTempo
        contTempo -= 1  

    if (somaCont == 55) and (not comecou):
        servidor.sendto('o jogo começou!'.encode(),('localhost',porta))
    elif (somaCont == 55) and comecou:
        servidor.sendto('o jogo começou!'.encode(),('localhost',porta))
        
    tempoInterrompido = True
    print('cronometro fechado')

#muita coisa abaixo tem que virar função e tbm organizar melhor
def inicio(): #o jogo ainda não começou
    global contTempo, porta, comecou, tempoInterrompido

    while True:
        
        msgBytes, endCliente = recebe()
        if msgBytes == 'Conectado: ':
            if endCliente not in jogadores:
                jogadores.append(endCliente)
            enviaTodos([endCliente], 'Digite "start" para começar: \n') #vai enviar só para o que acabou de entrar essa msg (pq é uma lista com um nome só)

        print(msgBytes, endCliente) #debugando

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos): 
            jogadoresProntos.append(endCliente)
            enviaTodos([endCliente], 'Sua partida está prestes a começar\n')
            if len(jogadoresProntos) >= 2:
                contTempo = 0 #reinicia o cronometro pq esse jogador acabou de entrar
                time.sleep(1) #tempo de processamento pra a funcao cronometro ser interrompida por completo
                Thread(target=cronometro).start() #inicia o contador outra vez, atraves dessa thread é possivel que um jogador interrompa em tempo real o cronometro           
        print(jogadoresProntos) #debug
        
        if endCliente[1] == porta: #termina essa parte de esperar jogadores e vai iniciar o jogo.
            Thread(target=jogando).start()
            tempoInterrompido = False
            comecou = True
            break

def jogando(): #lembrar de impedir que não conseguiu se conectar de responder (apesar de que as perguntas só são enviadas para os jogadoresProntos)
    print('entrou em jgando')
    global contTempo, jogadoresProntos, tempoInterrompido, perguntaSortida, numRodada
  
    while numRodada < 5:

        enviaTodos(jogadoresProntos, perguntaSortida[numRodada][0])
        time.sleep(1)
        Thread(target=cronometro).start()

        while not tempoInterrompido:
        
            #print(perguntaSortida[i][1], i)
            msgBytes, endCliente = recebe()
            if endCliente[1] == porta:
                print(' o cronometro zerou e ninguem acertou')
                break

            print('testando ', msgBytes, ' ', perguntaSortida[numRodada][1])
            if msgBytes == perguntaSortida[numRodada][1]:
                enviaTodos(jogadoresProntos, 'endCliente acertou\n')
                contTempo = 0
                time.sleep(0.5) #tempo pra processamento
                
            elif msgBytes != perguntaSortida[numRodada ][1]:
                print('diminuir ponto de quem errou\n')
        
        numRodada += 1
        tempoInterrompido = False
        
Thread(target=inicio).start()




