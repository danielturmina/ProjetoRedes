from socket import socket, AF_INET, SOCK_DGRAM
import threading
import time

class Client:
    def __init__(self):
        self.client_sock = socket(AF_INET, SOCK_DGRAM)
        self.server_address = ('localhost', 8080) # put the Server's IP on "localhost"
        #self.name = str(input('name: '))
        #self.client_sock.sendto(self.name.encode(), self.server_address)
        self.quit = False
        print('chat server, have fun!')
        self.continua = False #teste
        self.mensagem = '' #teste
        thread_receive = threading.Thread(target=self.receive).start()
        thread_send = threading.Thread(target=self.send).start()
        thread_escreve = threading.Thread(target=self.escreve).start()

    def receive(self):
        #time.sleep(3)
        #self.quit = True
        while True:
            if self.continua:
                print(self.mensagem.upper())
                self.continua = False
                print('debug Receive')


    def send(self):
        while True:
            if self.quit:
                break
            self.mensagem = input('')
            self.continua = True
            print('debug send\n')

    def escreve(self):
        while True:
            time.sleep(5)
            print('verificando se recebo mensgaem do servidor com input aberto do "send"')


client_sock = Client()