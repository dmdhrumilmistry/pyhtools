'''
module: generator.py
description: generates evil file executable
'''
from enum import Enum
from subprocess import call
from os import name as os_name
# from nuitka.Tracing import options_logger

# supress options 
# options_logger.is_quiet = True 
# above changes are redundant here,
# since, nuitka will load Tracing module on its own.
# Hence, changes are required in nuitka module as shown below
# options_logger = OurLogger("Nuitka-Options", quiet=True)


class Compilers(Enum):
    DEFAULT = 0
    MINGW = 1
    CLANG = 2


class ExecutableGenerator:
    '''
    class to create executable from python script
    '''

    def __init__(self, file_path: str, output_dir: str = None, icon: str = None, compiler: Compilers = Compilers.DEFAULT, onefile: bool = True, remove_output: bool = True, window_uac_perms:bool=False, disable_console:bool=True, company_name:str='DMSec', product_name:str='pyhtools', product_version:str='0.1.0') -> None:
        '''Executable Generator constructor
        
        Args:
            file_path (str): path of python script
            output_dir (str): path where executable generate will be stored. Default value is None
            compiler (Compilers): compiler type. default value is DEFAULT from Compliers. Others include MINGW and CLANG
            onefile (bool): generates only single executable file
            remove_output (bool): remove temporary directories after compilation of executable
            window_uac_perms (bool): Windows specific option to get UAC admin permissions before running executable. Default value is False
            disable_console (bool): avoids opening console when user runs the program. Doesn't work on linux distros
            company_name (str): name of the company, default value: DMSec
            product_name (str): name of the product, default value: pyhtools
            product_version (str): product version as string

        Returns:
            None
        '''
        # file options
        self.__file = file_path

        # set options
        self.__options = {
            'onefile': onefile,
            'remove-output': remove_output,
            'output-dir': output_dir,
            'disable-console': disable_console,
            'company-name':company_name,
            'product-name':product_name,
            'product-version':product_version,
            'standalone': True,
            'assume-yes-for-downloads': True,
        }

        # os based options
        if os_name == 'nt':
            self.__options['icon'] = icon
            self.__options['windows-uac-admin'] = window_uac_perms
        else:
            self.__options['linux-icon'] = icon

        # compiler based options
        if compiler == Compilers.CLANG:
            self.__options['clang'] = True
        elif compiler == Compilers.MINGW:
            self.__options['mingw'] = True

    def __generate_command(self):
        '''
        generates nuitka command

        Args:
            None

        Returns:
            None
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
        '''Generates executable file from specified configuration
        
        Args:
            None

        Returns:
            int: returns int 0 if compilation was successfuly else any other code 
        '''
        # linux devices requires patchelf to be installed
        # sudo apt install patchelf 
        command = self.__generate_command()

        # vuln: os command injection
        return call(command, shell=True, )
