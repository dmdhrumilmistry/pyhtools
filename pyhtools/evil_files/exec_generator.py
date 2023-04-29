'''
module: generator.py
description: generates evil file executable
'''
from enum import Enum
from subprocess import call
from os import name as os_name


class Compilers(Enum):
    DEFAULT = 0
    MINGW = 1
    CLANG = 2


class ExecutableGenerator:
    '''
    creates executable from python script.
    '''

    def __init__(self, file_path: str, output_dir: str = None, icon: str = None, compiler: Compilers = Compilers.DEFAULT, onefile: bool = True, remove_output: bool = True,) -> None:
        # file options
        self.__file = file_path

        # set options
        self.__options = {
            'onefile': onefile,
            'standalone': True,
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
        '''
        generates nuitka command
        '''
        if os_name == 'nt':
            command = 'python -m nuitka '
        else:
            command = 'python3 -m nuitka '

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
        # linux devices requires patchelf to be installed
        # sudo apt install patchelf 
        command = self.__generate_command()

        # vuln: os command injection
        return call(command, shell=True)
