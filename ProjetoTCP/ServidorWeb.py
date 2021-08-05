"""Projeto 2: Servidor Web (implemente o protocolo padronizado HTTP/1.1) - TCP
● Deverá ser desenvolvido um servidor WEB OK;
● Deverá implementar o protocolo HTTP/1.1, apenas o método GET;
● O servidor terá que ser capaz de retornar diversos tipos de arquivos (por ex: html, htm, css, js, png, jpg, svg...);
● Ou seja, deverá conseguir manipular tanto arquivos de texto, quanto arquivos binários;
● O servidor deverá ser capaz de transmitir arquivos de tamanho muito grande
● Os requisitos mínimos (devem ser implementados obrigatoriamente) são o desenvolvimento das respostas com os códigos de resposta a seguir:
            ○ 200 OK
                    ■ Requisição bem-sucedida, objeto requisitado será enviado
            ○ 400 Bad Request OK
                    ■ Mensagem de requisição não entendida pelo servidor, nesse caso o cliente escreveu a mensagem de requisição com algum erro de sintaxe OK
            ○ 404 Not Found
                    ■ Documento requisitado não localizado no servidor
            ○ 505 HTTP Version Not Supported OK
                    ■ Versão do HTTP utilizada não é suportada neste servidor OK
● Com exceção do código 200, o servidor deverá enviar obrigatoriamente um arquivo html personalizado informando o respectivo erro;
● Se a pasta requisitada não contiver um arquivo index.html ou index.htm, o servidor deverá criar uma página html para navegar pelas pastas, semelhante ao que ​apache​ faz
(que navega nas pastas de forma semelhante ao windows explorer, nautilus e afins...);
● O servidor Web deverá ler os arquivos de uma pasta específica, caso ela não exista, deverá ser criada automaticamente ao executar o servidor; OK
● O uso de sockets TCP é obrigatório. OK"""


from socket import socket, AF_INET, SOCK_STREAM
import os
from datetime import *
import datetime
import time


caminho_base = os.getcwd()
if not os.path.isdir(caminho_base+'\pastaEspecifica'):
    os.mkdir(caminho_base+'\pastaEspecifica')
caminho_base = caminho_base+'\pastaEspecifica'
print(caminho_base)

def mostraDiretorio():
    caminho = os.getcwd()
    caminhos = [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
    
    paginaHtml = '''<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YD redes</title>
        </head>
        <body>
        <table>
        <tr>
        <th>Nome</th>
        <th>Ultima Modificação</th>
        <th>Tamanho</th>
        </tr>
        '''

    for i in caminhos:
        indexBarra = i.rfind('\\')
        tamanhoCaminho = os.path.getsize(i)
        horaCaminho = os.path.getctime(i)
        ano,mes,dia,hora,minuto,segundos=time.localtime(horaCaminho)[:-3]
        horario = "%02d/%02d/%d %02d:%02d:%02d"%(dia,mes,ano,hora,minuto,segundos)
        
        paginaHtml += f'''  <tr>
                    <td><a href= {f'/{i[indexBarra+1:]}'}>{f'{i[indexBarra + 1:]}'}</td>
                    <td align= "right">{horario}</td>
                    <td align= "right">{f'{round((tamanhoCaminho/1024),2)} MB'}</td>
                    <td>&nbsp;</td>
                </tr>'''
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
    print(lista)
    for x in lista:
        caminho_requisitado_final = os.path.join(caminho_base, x) #Join para se livrar do problema das \ / (Win x Linux)
        caminho_base = caminho_requisitado_final
    caminho_base = os.getcwd()
    print(caminho_base)
    print(caminho_requisitado_final)


#ERRO 400 - PODE OCORRER TANTO DIFERENTES TIPO DE ERRO DE SINTAXE, COMO SABER?

    mensagem_de_resposta = ''   #coloquei porque dava um erro quando coloquei os condicionais para cada requisição dentro do "else"
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

    else:  #AQUI FAREMOS O 400, O 200 E O NAVEGARO POR PASTAS
        
        paginaHtml = mostraDiretorio()
        
        if caminho_requisitado == '/':
            mensagem_de_resposta = ''
            mensagem_de_resposta += 'HTTP/1.1 200 OK\r\n'
            mensagem_de_resposta += 'Date: Thu, 01 Jul 2021 21:11:19 GMT\r\n'
            mensagem_de_resposta += 'Server: CIn/UFPE/0.0.0.1 (Ubuntu)\r\n'
            mensagem_de_resposta += f'Content-Length: {len(paginaHtml)}\r\n'
            mensagem_de_resposta += 'Content-Type: text/html\r\n'
            mensagem_de_resposta += '\r\n'

            mensagem_de_resposta += paginaHtml
                       

        if caminho_requisitado == '/teste': #alterei
            html = ''
            html += '<html><head><title>Fica feliz chrome</title></head>'
            html += '<body>'
            html += '<h1 style="color:red">Essa pagina eh um exemplo</h1>'
            html += f'<h2 style="color:gray">Cliente o seu endereco eh: {cliente_endereco}</h2>'
            html += '</body></html>'

            mensagem_de_resposta = ''
            mensagem_de_resposta += 'HTTP/1.1 200 OK\r\n'
            mensagem_de_resposta += 'Date: Thu, 01 Jul 2021 21:11:19 GMT\r\n'
            mensagem_de_resposta += 'Server: CIn/UFPE/0.0.0.1 (Ubuntu)\r\n'
            mensagem_de_resposta += f'Content-Length: {len(html)}\r\n'
            mensagem_de_resposta += 'Content-Type: text/html\r\n'
            mensagem_de_resposta += '\r\n'

            mensagem_de_resposta += html
        
        else:
            if caminho_requisitado != '/favicon.ico':
                if os.path.isdir(caminho_requisitado_final):

                    paginaHtml = '''<!DOCTYPE html>
                    <html lang="pt-br">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>YD redes</title>
                    </head>
                    <body>
                    <table>
                    <tr>
                    <th>Nome</th>
                    <th>Ultima Modificação</th>
                    <th>Tamanho</th>
                    </tr>
                    '''
                    for i in os.listdir(caminho_requisitado_final):
                        paginaHtml += f'''  <tr>
                                    <td><a href= {i}>{f'{i}'}</td>
                                    
                                    <td>&nbsp;</td>
                                </tr>'''
                    paginaHtml += '''</table>
                            </body>
                            </html>'''

                    page = ('HTTP/1.1 200 OK\r\n'
                            'Date: Thu, 01 Jul 2021 21:11:19 GMT\r\n'
                            'Server: servidordotchan/0.0.1 (Windows)\r\n'
                            'Content-Type: text/html\r\n'
                            f'Content-Length: {len(paginaHtml)}\r\n'
                            '\r\n')
                    mensagem_de_resposta += page + paginaHtml

                    print('dir ', os.listdir(caminho_requisitado_final), 'caminho base :', caminho_base)

                    #print('entrou na parte de pasta', mensagem_de_resposta)
                    
                    
                else:
                    #arquivo = open('C:\\Users\\YNC\\Documents\\GitHub\\ProjetoRedes\\ProjetoTCP\\teste.py', 'r')
                    arquivo = open(caminho_requisitado_final, 'r')
                    arquivoLido = arquivo.read()
                    print(arquivoLido)
                    arquivo.close()

                    page = ('HTTP/1.1 200 OK\r\n'
                            'Date: Thu, 01 Jul 2021 21:11:19 GMT\r\n'
                            'Server: servidordotchan/0.0.1 (Windows)\r\n'
                            'Content-Type: text/html\r\n'
                            f'Content-Length: {len(arquivoLido)}\r\n'
                            '\r\n')
                    mensagem_de_resposta += page + arquivoLido

    
    cliente_socket.send(mensagem_de_resposta.encode())
    #input('')


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