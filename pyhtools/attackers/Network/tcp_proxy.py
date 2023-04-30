from functools import wraps
from threading import Thread

import os
import socket
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class TCProxy:
    '''TCP proxy'''
    def __init__(self, filepath: str = None) -> None:
        '''TCProxy class constructor
        
        Args: 
            filepath: path to file for storing captured data

        Returns: 
            None
        '''
        self.__file_name = filepath

        if self.__file_name and os.path.isfile(self.__file_name):
            logging.warning(
                f'{self.__file_name} file data will be overwritten!')
            with open(self.__file_name, 'wb') as f:
                f.write(b'')

        elif self.__file_name:
            logging.info(
                f'Captured data will be saved in file {self.__file_name}')

    def receive_from(self, conn: socket.socket):
        '''Accepts socket data and returns data from the buffer
        
        Args:
            conn (socket.socket): socket connection for reception

        Returns:
            bytes: returns received data
        '''
        conn.settimeout(5)
        try:
            buff = b''
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buff += data
        except Exception:
            pass
        return buff

    @staticmethod
    def handler(func):
        '''decorator used for packet modification
        
        Args:
            func (function): method function to be wrapped 

        Returns:
            function: wrapped function with error handling
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = None
            try:
                res = func(**args, **kwargs)
                return res
            except Exception as e:
                logging.error(e)

        return wrapper

    @handler
    def request_handler(self, buff: bytes):
        '''manipulate buffer data before sending request to remote host
        
        Args:
            buff (bytes): received data

        Returns:
            bytes: received data after handling request
        '''
        return buff

    @handler
    def response_handler(self, buff: bytes):
        '''manipulate buffer data after receiving from remote host
        
        Args:
            buff (bytes): received data

        Returns:
            bytes: received data after handling request
        '''
        return buff

    def __write_data(self, data):
        '''Write Data to file
        
        Args:
            data (bytes): data to be written to the file
        
        Returns:
            None
        '''
        if not isinstance(data, bytes):
            data = bytes(data, encoding='utf-8')

        if self.__file_name:
            with open(self.__file_name, 'ab') as f:
                f.write(data)

    def proxy_handler(self, client_sock: socket.socket, remote_host: str, remote_port: int, receive_first: bool, v4: bool = True):
        '''handles proxy connections
        
        Args:
            client_sock (socket.socket): client TCP socket connection
            remote_host (str): IP address of the remote host
            remote_port (int): port of remote host
            receive_first (bool): if True proxy will start receiving data else it'll send
            v4 (bool): if True uses IP v4 address else IP v6

        Returns:
            None
        '''
        address_family = socket.AF_INET if v4 else socket.AF_INET6
        remote_sock = socket.socket(address_family, socket.SOCK_STREAM)
        remote_sock.connect((remote_host, remote_port))
        remote_buff = b''

        if receive_first:
            remote_buff = self.receive_from(client_sock)
            self.__write_data(remote_buff)

        remote_buff = self.response_handler(remote_buff)
        if len(remote_buff):
            logging.info(f'[<--] Send {len(remote_buff)} bytes to localhost')
            client_sock.send(remote_buff)

        while True:
            # data from localhost to remote
            local_buff = self.receive_from(client_sock)
            if len(local_buff):
                logging.info(
                    f'[-->] Received {len(local_buff)} bytes from localhost')
                local_buff = self.request_handler(local_buff)
                remote_sock.send(local_buff)
                logging.info(f'[-->] Sent to remote host')

            # data from remote to localhost
            remote_buff = self.response_handler(remote_buff)
            if len(remote_buff):
                logging.info(
                    f'[<--] Received {len(remote_buff)} bytes from remote host')
                client_sock.send(remote_buff)

                remote_buff = self.response_handler(remote_buff)
                client_sock.send(remote_buff)
                logging.info(f'[<--] Sent to localhost')

            # if no data is received close sockets
            if not len(local_buff) or not len(remote_buff):
                remote_sock.close()
                client_sock.close()
                logging.info('Closing connections due to no incoming data')
                break

    def serve_proxy(self,  remote_host: str, remote_port: int, host: str = '0.0.0.0', port: int = 8080, max_conns: int = 5, receive_first: bool = False, v4: bool = True):
        '''Starts Proxy Server
        
        Args:
            remote_host (str): IP address of the remote host
            remote_port (int): port of remote host
            host (str): ip address of binding interface (default = '0.0.0.0', listens on all interfaces)
            port (int): port address of binding interface
            max_conns (int): maximum number of connections to listen for
            receive_first (bool): if True proxy will start receiving data else it'll send
            v4 (bool): if True uses IP v4 address else IP v6

        Returns:
            None
        '''
        address_family = socket.AF_INET if v4 else socket.AF_INET6
        server = socket.socket(address_family, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((host, port))
        except Exception as e:
            logging.error(f'Cannot bind: {e}')

        logging.info(
            f'Listening on {host}:{port} with maximum {max_conns} connections')
        server.listen(max_conns)

        while True:
            # accept client connection request
            client_sock, addr = server.accept()
            logging.info(f'Incoming from {addr[0]}:{addr[1]}')

            # start proxy thread
            # proxy_handler(self, client_sock: socket.socket, remote_host: str, remote_port: int, receive_first: bool, v4: bool = True)
            thread = Thread(target=self.proxy_handler, args=(
                client_sock, remote_host, remote_port, receive_first, v4))
            try:
                thread.start()
            except Exception as e:
                logging.error(f'Error in Thread: {e}')


if __name__ == '__main__':
    proxy = TCProxy()
    proxy.serve_proxy(
        remote_host='github.com',
        remote_port=443,
        host='0.0.0.0',
        port=8080,
        max_conns=5,
        receive_first=True,
        v4=True,
    )
