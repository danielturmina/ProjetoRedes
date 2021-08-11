from socket import socket, AF_INET, SOCK_STREAM

sock = socket(AF_INET, SOCK_STREAM)

servidor_endereco = 'localhost',8081

sock.connect(servidor_endereco)

messagem_enviada = 'POST /nova HTTP/1.1\r\n'
messagem_enviada += 'Host: localhost\r\n'
messagem_enviada += '\r\n'

sock.send(messagem_enviada.encode())

mensagem_recebida = sock.recv(2048)

print(mensagem_recebida.decode())