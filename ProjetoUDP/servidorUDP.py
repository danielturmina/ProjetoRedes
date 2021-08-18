""" 
Projeto 1: Quiz Competitivo
dft@cin.ufpe.br
ycb@cin.ufpe.br
"""

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import random
import time

jogadores = []
jogadoresProntos = []
perguntaSortida = [] 
comecou = False
dicNomes = {} 
dicPontuacao = {}
porta = 12000 
contTempo = 10

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

arquivo = open('ProjetoUDP/campeoes.txt', "r") 
perguntas = lerArquivo(arquivo)
arquivo.close()

sorteio = random.sample(range(0,19), 5) 
for i in sorteio: 
    perguntaSortida.append(perguntas[int(i)]) 

print('Servidor iniciado, perguntas sorteadas e aguardando conexões.')

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
    print('Iniciando cronômetro...')
    while contTempo > 0:
        
        time.sleep(1)
        if not comecou and contTempo == 0:
            enviaTodos(jogadoresProntos, str("Novo jogador entrou na sala, o tempo será reiniciado!"))
        if not comecou and contTempo != 0: 
            enviaTodos(jogadoresProntos, str(contTempo))
        somaCont += contTempo
        contTempo -= 1  

    if somaCont == 55:
        servidor.sendto('o jogo começou!'.encode(),('localhost',porta))
    
    print('Cronômetro fechado')

def cronometro2(): 
    print('Iniciando cronômetro...')
    global contTempo, porta, comecou
    contTempo = 10 
    somaCont2 = 0

    while contTempo > 0:
        time.sleep(1)
        somaCont2 += contTempo
        contTempo -= 1  
    
    servidor.sendto('o cronômetro zerou!'.encode(),('localhost',porta))      

def inicio(): 
    global contTempo, porta, comecou 

    while True:      
        msgBytes, endCliente = recebe()
        if msgBytes[:11] == 'Conectado: ': 
            if endCliente not in jogadores:
                jogadores.append(endCliente)
                dicNomes[endCliente] = msgBytes[11:] 
                                              
            enviaTodos([endCliente], '100')

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (len(jogadoresProntos) == 5): 
            enviaTodos([endCliente], '102')

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (len(jogadoresProntos) < 5):
            jogadoresProntos.append(endCliente)
            dicPontuacao[endCliente] = [None,None,None,None,None]
            enviaTodos([endCliente], '101')
            if len(jogadoresProntos) >= 2:
                contTempo = 0 
                time.sleep(1) 
                Thread(target=cronometro).start()         
            print('Jogadores Prontos: ',jogadoresProntos)
        
        if endCliente[1] == porta: 
            Thread(target=jogando).start()
            comecou = True
            break

novosJogadores = []

def esperaRetorno():
    global novosJogadores, jogadoresProntos, jogadores
    contRetorno = 0
    flagRetorno =  True
    jogadoresDesconectados = []

    while flagRetorno:
        msg, end = recebe()
        if (end not in novosJogadores) and (end not in jogadoresDesconectados):
            if msg == 's':
                enviaTodos([end], '500')
                novosJogadores.append(end)
            else:
                enviaTodos([end], '501') 
                jogadoresDesconectados.append(end)
            contRetorno += 1

        elif end in novosJogadores:
            enviaTodos([end], '502')
        
        if contRetorno >= len(jogadores):
            flagRetorno = False

    if len(novosJogadores) == 0:
        return False
    else:
        return True

def jogando(): 
    global contTempo, jogadoresProntos, perguntaSortida, dicPontuacao, jogadores, dicNomes, comecou, novosJogadores
  
    for numRodada in range(5):
        enviaTodos(jogadoresProntos, perguntaSortida[numRodada][0])
        time.sleep(1)
        Thread(target=cronometro2).start()

        while True:   
            msgBytes, endCliente = recebe()
            
            if endCliente[1] == porta:
                print('Cronômetro fechado')
                break

            elif (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (comecou == True):
                enviaTodos([endCliente], '103')   

            elif msgBytes[:11] == 'Conectado: ' and (endCliente not in jogadoresProntos) and (comecou == True):
                enviaTodos([endCliente], '104')    

            elif (endCliente in jogadoresProntos) and msgBytes == perguntaSortida[numRodada][1]:  
                print('O jogador:',dicNomes[endCliente],'acertou a pergunta')    
                msg1 = 'O jogador: '+str(dicNomes[endCliente])+' acertou!\n'
                enviaTodos([endCliente], '200')   
                enviaTodos(jogadoresProntos, msg1)
                if dicPontuacao[endCliente][numRodada] == None:
                    dicPontuacao[endCliente][numRodada] = 0
                dicPontuacao[endCliente][numRodada] += 25
                contTempo = 0            
                
            elif (endCliente in jogadoresProntos) and msgBytes != perguntaSortida[numRodada][1]:
                enviaTodos([endCliente], '300')
                print('O jogador:',dicNomes[endCliente],'errou a pergunta') 
                if dicPontuacao[endCliente][numRodada] == None:
                    dicPontuacao[endCliente][numRodada] = 0
                dicPontuacao[endCliente][numRodada] -= 5

    n = 1
    dicPontosFinais = {}
    contPontos = 0

    for i in dicPontuacao:
        for x in dicPontuacao[i]:
            if x != None:
                contPontos += x
            else:
                contPontos -=1
        dicPontosFinais[i] = contPontos    
        contPontos = 0
    for i in sorted(dicPontosFinais, key = dicPontosFinais.get, reverse=True): 
        msgFinal = str(n)+"° Lugar: "+str(dicNomes[i])+" com "+str(dicPontosFinais[i])+" pontos!"
        enviaTodos(jogadoresProntos, msgFinal)
        n += 1
    enviaTodos(jogadoresProntos, '\nFim de Jogo - Obrigado!!\n')
    enviaTodos(jogadores, '400')
    novosJogadores = []
    retorno = esperaRetorno()
    
    if retorno:
        jogadores = []
        jogadoresProntos = []
        perguntaSortida = [] 
        comecou = False
        dicNomes = {} 
        dicPontuacao = {}
        contTempo = 10          
        arquivo = open('ProjetoUDP/campeoes.txt', "r") 
        perguntas = lerArquivo(arquivo)
        arquivo.close()
        sorteio = random.sample(range(0,19), 5) 

        for i in sorteio: 
            perguntaSortida.append(perguntas[int(i)]) 

        enviaTodos(novosJogadores, '600')
        Thread(target=inicio).start()
    
    else:
        jogoContinua = False
    
Thread(target=inicio).start()