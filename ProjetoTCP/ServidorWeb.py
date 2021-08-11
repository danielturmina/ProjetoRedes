"""Projeto 2: Servidor Web (implemente o protocolo padronizado HTTP/1.1) - TCP
● Deverá ser desenvolvido um servidor WEB OK;
● Deverá implementar o protocolo HTTP/1.1, apenas o método GET; OK
● O servidor terá que ser capaz de retornar diversos tipos de arquivos (por ex: html, htm, css, js, png, jpg, svg...); ????
● Ou seja, deverá conseguir manipular tanto arquivos de texto, quanto arquivos binários; ???
● O servidor deverá ser capaz de transmitir arquivos de tamanho muito grande ????
● Os requisitos mínimos (devem ser implementados obrigatoriamente) são o desenvolvimento das respostas com os códigos de resposta a seguir:
            ○ 200 OK   OK
                    ■ Requisição bem-sucedida, objeto requisitado será enviado OK
            ○ 400 Bad Request OK
                    ■ Mensagem de requisição não entendida pelo servidor, nesse caso o cliente escreveu a mensagem de requisição com algum erro de sintaxe OK
            ○ 404 Not Found OK
                    ■ Documento requisitado não localizado no servidor OK
            ○ 505 HTTP Version Not Supported OK
                    ■ Versão do HTTP utilizada não é suportada neste servidor OK
● Com exceção do código 200, o servidor deverá enviar obrigatoriamente um arquivo html personalizado informando o respectivo erro; OK
● Se a pasta requisitada não contiver um arquivo index.html ou index.htm, o servidor deverá criar uma página html para navegar pelas pastas, semelhante ao que ​apache​ faz
(que navega nas pastas de forma semelhante ao windows explorer, nautilus e afins...); OK
● O servidor Web deverá ler os arquivos de uma pasta específica, caso ela não exista, deverá ser criada automaticamente ao executar o servidor; OK
● O uso de sockets TCP é obrigatório. OK"""


from socket import socket, AF_INET, SOCK_STREAM
import os
from datetime import *
import time
from mimetypes import guess_type

#SE ARQUIVO TEM ESPACO OU ACENTO BUGA MAS ACHO QUE ISSO DA PARA PASSAR DE BOA
#VERIFICAR SE OCORRER ERROS DE /favicon.ico
#VERIFICAR SE OCORRER ERROS DE versao = colunas[2][5:8] linha 103 dando vazio depois de um tempo com o servidor rodando
#EU VI NO DOS MENINOS QUE ELES COLOCARAM OS IF ANTES DE TUDO PARA PASSAR DESSES DOIS ERROS

#AQUI SE livra do problema das \ / (Win x Linux)?
caminho_base = os.getcwd() 
if not os.path.isdir(caminho_base+'\ProjetoTCP\pastaEspecifica'):
    os.mkdir(caminho_base+'\ProjetoTCP\pastaEspecifica')
caminho_base = caminho_base+'\ProjetoTCP\pastaEspecifica'
print(caminho_base)

def mostraDiretorio(caminho_base,caminho_requisitado, caminho_requisitado_final):
    paginaHtml = f'''<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YD Server</title>
        </head>
        <body>
        <h1>Index of {caminho_requisitado}</h1>
        <table>
        <tr>
        <th>Nome</th>
        <th>Ultima Modificação</th>
        <th>Tamanho</th>
        </tr>
       '''
    teste = os.listdir(caminho_requisitado_final)
    print(teste)
    for p in teste:
                    arquivoPasta = os.path.join(caminho_requisitado_final, p)
                    arq =os.path.join(caminho_requisitado, p)
                    tamanho = os.path.getsize(arquivoPasta)
                    horaCaminho = os.path.getctime(arquivoPasta)
                    ano,mes,dia,hora,minuto,segundos=time.localtime(horaCaminho)[:-3]
                    horario = "%02d/%02d/%d %02d:%02d:%02d"%(dia,mes,ano,hora,minuto,segundos)
                    if not os.path.isdir(arquivoPasta):
                        paginaHtml += f'''
                                <tr>
                                    <td><a href= {f'{arq}'}>{os.path.basename(arquivoPasta)}</td>
                                    <td align= "right">{horario}</td>
                                    <td align= "right">{f'{round((tamanho/1024),2)} KB'}</td>
                                    <td>&nbsp;</td>
                                </tr>'''
                    else:
                        paginaHtml += f'''
                                <tr>
                                    <td><a href= {f'{arq}'}>{os.path.basename(arquivoPasta)}</td>
                                    <td align= "right">{horario}</td>
                                    <td align= "right"></td>
                                    <td>&nbsp;</td>
                                </tr>
                        '''
    paginaHtml += '''</table>
            </body>
          </html>'''

    return paginaHtml

def atender_cliente(cliente_socket, cliente_endereco):
    global caminho_base
    dados_binarios = cliente_socket.recv(2048)

    print('Mensagem recebida: ')

    mensagem_recebida = dados_binarios.decode()
    print('msg recebida: ', mensagem_recebida)

    print('\n\nDetalhamento da requisição:')
    linhas = mensagem_recebida.split('\n')
    primeira_linha = linhas[0].strip()
    colunas = primeira_linha.split(' ')
    versao = colunas[2][5:8]
    tipo_requisicao = colunas[0]
    caminho_requisitado = colunas[1]
    print('tipo de requisicao: ', tipo_requisicao)
    print('caminho requisitado: ', caminho_requisitado)
    print('versao: ', versao)
    lista = caminho_requisitado.split('/')
    print('Lista Caminho',lista)
    for x in lista:
        caminho_requisitado_final = os.path.join(caminho_base, x) #Join para se livrar do problema das \ / (Win x Linux)
        caminho_base = caminho_requisitado_final
    caminho_base = os.getcwd()
    caminho_base = caminho_base+'\ProjetoTCP\pastaEspecifica'
    print('Caminho Base: ',caminho_base)
    print('Caminho Final: ',caminho_requisitado_final)

    if versao != '1.0' and versao != '1.1':
        tempo = str(datetime.today().ctime())
        print(tempo)
        pagina =    ('HTTP/1.1 505 HTTP Version Not Supported\r\n'
                    'Date: '+tempo+'\r\n'
                    'Server: YD-Server Win 10\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
        pagina += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>505 HTTP Version Not Supported</title>
                    </head>
                    <body>
                        <h1>505 HTTP Version Not Supported</h1>
                        <h2>Versão do HTTP utilizada não é suportada neste servidor<h2>
                    </body>
                    </html>''')
        mensagem_de_resposta = pagina

        cliente_socket.send(mensagem_de_resposta.encode())
    elif  tipo_requisicao != 'GET':
        tempo = str(datetime.today().ctime())
        pagina =    ('HTTP/1.1 501 Not Implemented\r\n'
                    'Date: '+tempo+'\r\n'
                    'Server: YD-Server Win 10\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
        pagina += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>501 Not Implemented</title>
                    </head>
                    <body>
                        <h1>501 Not Implemented</h1>
                        <h2>Tipo de requisição não implementado no servidor<h2>
                    </body>
                    </html>''')
        mensagem_de_resposta  = pagina

        cliente_socket.send(mensagem_de_resposta.encode())

    #ERRO 400 - PODE OCORRER DIFERENTES TIPO DE ERRO DE SINTAXE, COMO SABER?
    elif caminho_requisitado[0] != "/":  #SERA QUE É ISSO??
        tempo = str(datetime.today().ctime())
        pagina =    ('HTTP/1.1 400 Bad Request\r\n'
                    'Date: '+tempo+'\r\n'
                    'Server: YD-Server Win 10\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
        pagina += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>400 Bad Request</title>
                    </head>
                    <body>
                        <h1>400 Bad Request</h1>
                        <h2>Mensagem de requisição não entendida pelo servidor<h2>
                    </body>
                    </html>''')
        mensagem_de_resposta  = pagina

        cliente_socket.send(mensagem_de_resposta.encode())
    elif not os.path.exists(caminho_requisitado_final):
        tempo = str(datetime.today().ctime())
        pagina =    ('HTTP/1.1 404 Not Found\r\n'
                    'Date: '+tempo+'\r\n'
                    'Server: YD-Server Win 10\r\n'
                    'Content-Type: text/html\r\n'
                    '\r\n')
        pagina += ('''
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>404 Not Found</title>
                    </head>
                    <body>
                        <h1>404 Not Found</h1>
                        <h2>Documento requisitado não localizado no servidor<h2>
                    </body>
                    </html>''')
        mensagem_de_resposta  = pagina

        cliente_socket.send(mensagem_de_resposta.encode())
    else:  
        if os.path.isdir(caminho_requisitado_final):
            verificaHtml= os.path.join(caminho_requisitado_final, 'index.html')
            verificaHtm= os.path.join(caminho_requisitado_final, 'index.htm')
            if os.path.exists(verificaHtml):
                #REVER PARA VERIFICAR SE É A MELHOR FORMA DE PEGAR DATA, TIPO E TAMANHO
                cabecalho = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(caminho_requisitado_final)}\r\n'
                    'Server: YD-Server Win 10\r\n'
                    f'Content-Type: {guess_type(caminho_requisitado_final)[0]}\r\n'
                    f'Content-lenght: {os.path.getsize(caminho_requisitado_final)}\r\n'
                    '\r\n')

                arq = open(verificaHtml, 'rb')
                arquivo = arq.read()
                arq.close()

                mensagem_de_resposta  = cabecalho.encode() + arquivo

                cliente_socket.send(mensagem_de_resposta)   
            elif os.path.exists(verificaHtm):
                #REVER PARA VERIFICAR SE É A MELHOR FORMA DE PEGAR DATA, TIPO E TAMANHO
                cabecalho = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(caminho_requisitado_final)}\r\n'
                    'Server: YD-Server Win 10\r\n'
                    f'Content-Type: {guess_type(caminho_requisitado_final)[0]}\r\n'
                    f'Content-lenght: {os.path.getsize(caminho_requisitado_final)}\r\n'
                    '\r\n')

                arq = open(verificaHtml, 'rb')
                arquivo = arq.read()
                arq.close()

                mensagem_de_resposta  = cabecalho.encode() + arquivo

                cliente_socket.send(mensagem_de_resposta)  
            else: #AQUI ENTRA NO PASSEAR PELAS PASTAS
                cabecalho = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(caminho_requisitado_final)}\r\n'
                    'Server: YD-Server Win 10\r\n'
                    f'Content-Type: {guess_type(caminho_requisitado_final)[0]}\r\n'
                    f'Content-lenght: {os.path.getsize(caminho_requisitado_final)}\r\n'
                    '\r\n')

                arquivo = mostraDiretorio(caminho_base,caminho_requisitado,caminho_requisitado_final)

                mensagem_de_resposta  = cabecalho + arquivo
                cliente_socket.send(mensagem_de_resposta.encode())  

        else:
            #REVER PARA VERIFICAR SE É A MELHOR FORMA DE PEGAR DATA, TIPO E TAMANHO
            cabecalho = ('HTTP/1.1 200 OK\r\n'
                    f'Date: {os.path.getatime(caminho_requisitado_final)}\r\n'
                    'Server: YD-Server Win 10\r\n'
                    f'Content-Type: {guess_type(caminho_requisitado_final)[0]}\r\n'
                    f'Content-lenght: {os.path.getsize(caminho_requisitado_final)}\r\n'
                    '\r\n')

            arq = open(caminho_requisitado_final, 'rb')
            arquivo = arq.read()
            arq.close()

            mensagem_de_resposta  = cabecalho.encode() + arquivo

            cliente_socket.send(mensagem_de_resposta)   
            

    cliente_socket.close()


servidor_socket = socket(AF_INET, SOCK_STREAM)

servidor_socket.bind(('localhost', 8081))

print('Socket criado')

servidor_socket.listen()

while True:
    print('Aguardando por novas requisições')
    _cliente_socket, _cliente_endereco = servidor_socket.accept()

    print('Requisição foi aceita. Aguardando o recebimento de mensagens.')
    atender_cliente(_cliente_socket, _cliente_endereco)