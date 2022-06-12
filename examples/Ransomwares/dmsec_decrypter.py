from pyhtools.evil_files.ransomwares.dmsec.decrypter import DMSecDecrypter

print('[*] Decrypting....')

# specify paths to be decrypted
PATHS = [r'paths_to_be_decrypted', ]

KEY = input('[+] Enter KEY : ')

# don't pass PATHS if all the drives are to be decrypted.
encrypter = DMSecDecrypter(KEY, PATHS)
encrypter.start()

print('[*] Decrypted...')
