""" 
● Deverá ser desenvolvido um jogo com competições ​online​ de perguntas e respostas; OK
● Um protocolo da camada de aplicação deverá ser desenvolvido e especificado no relatório;  ---------- ???
● Deverá ter pelo menos uma mensagem de requisição e pelo menos uma mensagem de resposta; OK
● O protocolo de transporte UDP deverá ser utilizado; OK
● Um servidor UDP deverá gerenciar as competições; OK
● Até 5 clientes UDP poderão participar de uma competição; OK
● Após a competição ser iniciada, não deverá ser permitido o ingresso de novos participantes; OK
● Cada competição terá 5 rodadas de perguntas e respostas; OK
● O servidor deverá ter um arquivo de texto contendo pelo menos 20 tuplas de perguntas e respostas; OK
○ As respostas deverão ser compostas por uma única palavra, com caracteres minúsculos; OK
○ O tema do Quiz ficará a critério da equipe; OK
● O servidor irá escolher aleatoriamente uma tupla de pergunta/resposta que será utilizada na rodada; OK
● Uma mesma competição não poderá ter duas tuplas repetidas; OK
● Cada rodada será encerrada quando algum participante acertar a resposta ou atingir uma duração máxima de 10 segundos; OK
● Pontuação de cada rodada:
○ Cada resposta errada: -5 pontos OK
○ Sem resposta: -1 ponto OK
○ Resposta correta: 25 pontos OK
● Após uma competição ser encerrada, um ​ranking​ com a pontuação é divulgado; OK
● e uma nova competição poderá ser iniciada. ------------------- FALTA IMPLEMENTAR
"""

#É necessário tratar nomes iguais?
#É necessário tratar empates?

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import random
import time


jogadores = []
jogadoresProntos = []
perguntaSortida = [] 
comecou = False
dicNomes = {} #Dicionario de nomes que vai ajudar na hora de imprimir os pontos finais
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

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (len(jogadoresProntos) == 5): #Enviando mensagem se alguem quiser se conectar e já tiver 5 jogadores prontos
            enviaTodos([endCliente], 'A quantidade limite de jogadores foi atingida! Tente novamente mais tarde!\n')

        if (msgBytes == 'start') and (endCliente not in jogadoresProntos) and (len(jogadoresProntos) < 5): #Limitando a Participação de 5 Pessoas
            jogadoresProntos.append(endCliente)
            dicPontuacao[endCliente] = [None,None,None,None,None]
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

            elif msgBytes == perguntaSortida[numRodada][1]:      
                msg1 = str(dicNomes[endCliente])+' acertou\n' #Coloquei para mostrar o nome de quem acertou
                enviaTodos(jogadoresProntos, msg1)
                dicPontuacao[endCliente][numRodada] = 25
                contTempo = 0            
                
            elif msgBytes != perguntaSortida[numRodada][1]:
                msg2 = "Você errou! Tente novamente...\n" #Mensagem mostrando que errou
                enviaTodos([endCliente], msg2)
                if dicPontuacao[endCliente][numRodada] == None:
                    dicPontuacao[endCliente][numRodada] = 0
                dicPontuacao[endCliente][numRodada] -= 5

    print(dicPontuacao) 
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
    for i in sorted(dicPontosFinais, key = dicPontosFinais.get, reverse=True): #O que fazer em caso de empate? Corrigir
        msgFinal = str(n)+"° Lugar: "+str(dicNomes[i])+" com "+str(dicPontosFinais[i])+" pontos!"
        enviaTodos(jogadoresProntos, msgFinal)
        n += 1
    enviaTodos(jogadoresProntos, '\nFim de Jogo - Obrigado!!\n')

   
Thread(target=inicio).start()
