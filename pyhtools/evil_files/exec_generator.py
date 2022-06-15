'''
module: generator.py
description: generates evil file executable
'''
from subprocess import call
from os import name as os_name
from enum import Enum


class Compilers(Enum):
    DEFAULT = 0
    MINGW = 1
    CLANG = 2


class ExecutableGenerator:
    '''
    creates executable
    '''

    def __init__(self, file_path: str, output_dir: str = None, icon: str = None, compiler: Compilers = Compilers.DEFAULT, onefile: bool = True, remove_output: bool = True,) -> None:
        # file options
        self.__file = file_path

        # set options
        self.__options = {
            'onefile': onefile,
            'standalone': True,
            'onefile': True,
            'remove-output': remove_output,
            'output-dir': output_dir,
        }

        # os based options
        if os_name == 'nt':
            self.__options['icon'] = icon
        else:
            icon = None

        # compiler based options
        if compiler == Compilers.CLANG:
            self.__options['clang'] = True
        elif compiler == Compilers.MINGW:
            self.__options['mingw'] = True

    def __generate_command(self):
        command = 'nuitka '
        for key in self.__options:
            cmd = ''
            value = self.__options[key]
            value_type = type(self.__options[key])

            # generate option
            if value_type is bool and value:
                cmd = f'--{key} '
            elif value_type is str:
                cmd = f'--{key}={value} '

            # add option to command
            command += cmd

        # add file name and return
        command += f'{self.__file}'
        return command

    def generate_executable(self):
        command = self.__generate_command()
        return call(command.split(), shell=True)
