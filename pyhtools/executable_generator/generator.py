'''
module: generator.py
description: generates evil files using specified payload and type
'''
from enum import Enum
# from subprocess import check_call, check_output


# TODO: convert all evil files modules into classes
# create new class object with parameters and generate
# evil file using specified compiler using subprocess


class CompileOptions(Enum):
    PYINTALLER = 0
    NUITKA = 1


class Generator:
    def __init__(self, _type: str, payload: str, compiler: CompileOptions = CompileOptions.PYINTALLER, *args, **kwargs) -> None:
        self.__type = _type
        self.__payload = payload
        self.__compiler = compiler

        self.__options = {
            'malwares': [
                'credential_harvester',
                'keylogger',
                'http_reverse_backdoor',
                'tcp_reverse_backdoor',
                'telegram_data_harvester',
                'telegram_remote_code_executor',
                'wireless_password_harvester'
            ],
            'ransomwares': [
                'dmsec',
            ],
            'worms': [
                'dir_cloner'
            ],
        }

    def verify():
        pass

    def show_options():
        pass

    def generate_file():
        pass
