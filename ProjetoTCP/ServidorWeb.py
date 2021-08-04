"""Projeto 2: Servidor Web (implemente o protocolo padronizado HTTP/1.1) - TCP
● Deverá ser desenvolvido um servidor WEB;
● Deverá implementar o protocolo HTTP/1.1, apenas o método GET;
● O servidor terá que ser capaz de retornar diversos tipos de arquivos (por ex: html, htm, css, js, png, jpg, svg...);
● Ou seja, deverá conseguir manipular tanto arquivos de texto, quanto arquivos binários;
● O servidor deverá ser capaz de transmitir arquivos de tamanho muito grande
● Os requisitos mínimos (devem ser implementados obrigatoriamente) são o desenvolvimento das respostas com os códigos de resposta a seguir:
            ○ 200 OK
                    ■ Requisição bem-sucedida, objeto requisitado será enviado
            ○ 400 Bad Request
                    ■ Mensagem de requisição não entendida pelo servidor, nesse caso o cliente escreveu a mensagem de requisição com algum erro de sintaxe
            ○ 404 Not Found
                    ■ Documento requisitado não localizado no servidor
            ○ 505 HTTP Version Not Supported
                    ■ Versão do HTTP utilizada não é suportada neste servidor
● Com exceção do código 200, o servidor deverá enviar obrigatoriamente um arquivo html personalizado informando o respectivo erro;
● Se a pasta requisitada não contiver um arquivo index.html ou index.htm, o servidor deverá criar uma página html para navegar pelas pastas, semelhante ao que ​apache​ faz
(que navega nas pastas de forma semelhante ao windows explorer, nautilus e afins...);
● O servidor Web deverá ler os arquivos de uma pasta específica, caso ela não exista, deverá ser criada automaticamente ao executar o servidor;
● O uso de sockets TCP é obrigatório."""


from socket import socket, AF_INET, SOCK_STREAM

def atender_cliente(cliente_socket, cliente_endereco):
    dados_binarios = cliente_socket.recv(2048)

    print('Mensagem recebida: ')

    mensagem_recebida = dados_binarios.decode()
    print(mensagem_recebida)

    print('\n\nDetalhamento da requisição:')
    linhas = mensagem_recebida.split('\n')
    primeira_linha = linhas[0].strip()
    colunas = primeira_linha.split(' ')

    print(f'Tipo da requisição: {colunas[0]}')
    print(f'Caminho requisitado: {colunas[1]}')
    print(f'Versão do HTTP: {colunas[2]}')

    print('Respondendo a requisição. Enviando um exemplo de código html.')

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

    cliente_socket.send(mensagem_de_resposta.encode())

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