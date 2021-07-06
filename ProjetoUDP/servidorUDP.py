from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import random
import time

jogadores = []
jogadoresProntos = []
perguntaSortida = [] 
comecou = False
dicNomes = {} #Dicionario de normes que vai ajudar na hora de imprimir os pontos finais
dicPontuacao = {}
#numRodada = 0
porta = 12000 
contTempo = 10
#tempoInterrompido = False

servidor = socket(AF_INET, SOCK_DGRAM)
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

def enviaTodos(lista, msg):
    for i in lista:
        servidor.sendto(msg.encode(), i)

def recebe():
    msgRecebida, endRecebido = servidor.recvfrom(2048) 
    msgRecebida = msgRecebida.decode()
    return [msgRecebida, endRecebido]

def cronometro(): 
    
    global contTempo, porta, comecou
    contTempo = 10 
    somaCont = 0

    while contTempo > 0:
        time.sleep(1)
        print(contTempo)
        if not comecou and contTempo == 0:
            enviaTodos(jogadoresProntos, str("Novo jogador entrou na sala, o tempo será reiniciado!"))
        if not comecou and contTempo != 0: #Nao vai aparecer 0 qnd um novo entrar, no meio da contagem
            enviaTodos(jogadoresProntos, str(contTempo))
        somaCont += contTempo
        contTempo -= 1  

    if somaCont == 55: #se 
        servidor.sendto('o jogo começou!'.encode(),('localhost',porta))
        
    #tempoInterrompido = True
    print('cronometro fechado')#debug

def cronometro2(): 
    
    global contTempo, porta, comecou #, tempoInterrompido
    contTempo = 10 
    somaCont2 = 0

    while contTempo > 0:
        time.sleep(1)
        print(contTempo)
        somaCont2 += contTempo
        contTempo -= 1  
    
    servidor.sendto('o cronometro zerou!'.encode(),('localhost',porta))      

def inicio(): 
    global contTempo, porta, comecou #, tempoInterrompido

    while True:
        
        msgBytes, endCliente = recebe()
        if msgBytes[:11] == 'Conectado: ': #Reconhecendo que conectou e sabendo que o jogador digitou o nome
            if endCliente not in jogadores:
                jogadores.append(endCliente)
                dicNomes[endCliente] = msgBytes[11:] #Pegando Nome da pessoas
            print(dicNomes)                     
                
            enviaTodos([endCliente], 'Digite "start" para começar:')

        print(msgBytes, endCliente) #debugando

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos): 
            jogadoresProntos.append(endCliente)
            dicPontuacao[endCliente] = 0
            enviaTodos([endCliente], 'Sua partida está prestes a começar\n')
            if len(jogadoresProntos) >= 2:
                contTempo = 0 
                time.sleep(1) 
                Thread(target=cronometro).start()         
        print(jogadoresProntos) #debug
        
        if endCliente[1] == porta: 
            Thread(target=jogando).start()
            #tempoInterrompido = False
            comecou = True
            break

def jogando(): 
    print('entrou em jgando') #debug
    global contTempo, jogadoresProntos, perguntaSortida 
  
    #while numRodada < 5:
    for numRodada in range(5):

        enviaTodos(jogadoresProntos, perguntaSortida[numRodada][0])
        time.sleep(1)
        Thread(target=cronometro2).start()

        while True:  
            
            msgBytes, endCliente = recebe()
            print('testando ', msgBytes, ' ', perguntaSortida[numRodada][1]) #debug
            
            if endCliente[1] == porta:
                print(' o cronometro zerou e ninguem acertou')
                break

            elif (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (comecou == True):   #Jogador tinha entrado, mas não digitou start a tempo
                enviaTodos([endCliente], 'Infelizmente você não digitou "start" a tempo, a partida já iniciou!')   

            elif msgBytes[:11] == 'Conectado: ' and (endCliente not in jogadoresProntos) and (comecou == True):   #Jogador NEM tinha entrado, ou seja NEM start apareceu
                enviaTodos([endCliente], 'Partida já iniciada, volte mais tarde!')    

            elif msgBytes == perguntaSortida[numRodada][1]:#Colocar Sem resposta!!!!!
                enviaTodos(jogadoresProntos, 'endCliente acertou\n')
                dicPontuacao[endCliente] += 25
                contTempo = 0            
                
            elif msgBytes != perguntaSortida[numRodada][1]:
                print('diminuir ponto de quem errou\n')
                dicPontuacao[endCliente] -= 5

    print(dicPontuacao) 
    n = 1
    for i in sorted(dicPontuacao, key = dicPontuacao.get, reverse=True): #O que fazer em caso de empate? Corrigir
        msgFinal = str(n)+"° Lugar: "+str(dicNomes[i])+" com "+str(dicPontuacao[i])+" pontos!"
        enviaTodos(jogadoresProntos, msgFinal)
        n += 1
    enviaTodos(jogadoresProntos, '\nFim de Jogo - Obrigado!!\n')

   
Thread(target=inicio).start()
