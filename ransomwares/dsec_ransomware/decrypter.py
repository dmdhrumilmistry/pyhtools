from cryptography.fernet import Fernet
from os.path import join, isfile
from os import getcwd, name, walk, chdir
from tempfile import gettempdir
from psutil import disk_partitions
from sys import exit


def get_partitions_path():
    '''
    get all mounted partition's mount point
    '''
    mount_points = []
    for partition in disk_partitions():
        mount_points.append(partition.mountpoint)
    return mount_points


def read_key(path):
    '''
    get key
    '''
    key_path = join(path, KEY_FILE)
    if isfile(key_path):
        cwd = getcwd()
        chdir(path)
        key = open(key_path, 'rb').read()
        chdir(cwd)
        return key
    else:
        print('[!] No key found!')
        exit()


def decrypt_file(file_path, key):
    '''
    decrypts specified file
    '''
    fernet = Fernet(key)
    enc_file_data = ''
    # read file data
    with open(file_path, 'rb') as file:
        enc_file_data = file.read()
    
    # encrypt file data
    file_data = fernet.decrypt(enc_file_data)

    # write encrypted file
    with open(file_path, 'wb') as file:
        file.write(file_data)


def decrypt_child_files(root_path, key):
    '''
    decrypts files inside specified root folder and it's subfolder
    '''
    for root, dirs, files in walk(root_path):
        chdir(root)
        
        for file in files:
            file_path = join(root, file)
            decrypt_file(file_path,key)


def start_recovery(paths:list):
    '''
    starts recovery process
    '''
    tempdir = gettempdir()
    KEY = read_key(KEY_PATH)
    for path in paths:
        decrypt_child_files(path, KEY)   


if __name__ == '__main__':
    path = input('[+] Enter Key Path : ')
    KEY_PATH = r'{}'.format(path)
    
    tempdir = gettempdir()
    KEY_FILE = 'key.dmsec'
    PATHS = get_partitions_path()

    start_recovery(PATHS)