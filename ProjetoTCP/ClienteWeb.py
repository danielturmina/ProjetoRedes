from socket import socket, AF_INET, SOCK_STREAM

sock = socket(AF_INET, SOCK_STREAM)

servidor_endereco = 'localhost',8081

sock.connect(servidor_endereco)

messagem_enviada = 'GET /imagem HTTP/2.0\r\n'
messagem_enviada += 'Host: localhost\r\n'
messagem_enviada += '\r\n'

sock.send(messagem_enviada.encode())

mensagem_recebida = sock.recv(2000)

print(mensagem_recebida.decode())