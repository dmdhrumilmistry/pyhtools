from cryptography.fernet import Fernet
from sys import exit
from os import walk
from os.path import join
from psutil import disk_partitions


class DMSecDecrypter:
    def __init__(self, key: str = None, paths: list = None) -> None:
        # check key
        if key == None:
            print('[!] Invalid KEY')
            exit()

        # convert key to bytes
        if type(key) == str:
            key = bytes(key, encoding='utf-8')
        self.KEY = key
        print('[!] Decrypting data using KEY :', self.KEY)

        # generate fernet obj for file encryption
        self.fernet = Fernet(self.KEY)

        # decrypt all partitions if paths are not passed
        if paths == None:
            self.PATHS = self.__get_partitions_path()
        else:
            self.PATHS = paths
        print('[!] PATHS to be decrypted :\n', self.PATHS)

    def __get_partitions_path(self) -> list:
        '''
        returns all mounted partition's mount points as a list
        '''
        mount_points = []
        for partition in disk_partitions():
            mount_points.append(partition.mountpoint)
        return mount_points

    def decrypt_file(self, file_path: str):
        '''
        decrypts single file
        '''
        try:
            # read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # decrypt file data
            dec_data = self.fernet.decrypt(file_data)

            # write file data
            with open(file_path, 'wb') as f:
                f.write(dec_data)
            print(f'[*] File {file_path} decrypted.')
            return True

        except Exception:
            print(f'[!] Failed to decrypt {file_path}')
            return False

    def decrypt_files(self, path: str):
        '''
        decrypts all the files in the specified path
        '''
        for root, dirs, files in walk(path):
            for file in files:
                file_path = join(root, file)
                self.decrypt_file(file_path=file_path)

    def start(self):
        for path in self.PATHS:
            self.decrypt_files(path)
