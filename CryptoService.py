import base64
import hashlib

from Cryptodome import Random
from Cryptodome.Cipher import AES


class CryptoService:
    def __init__(self, logger):
        self.logger = logger
        self.bs = AES.block_size
        self.key = hashlib.sha256(self.get_user_key(self.logger).encode()).digest()

    @staticmethod
    def get_user_key(logger):
        while True:
            key = input("Please type in a password to be used to encrypt/decrypt your default_token: ")
            confirmation = input("Please retype password: ")
            if key == confirmation:
                return key
            logger.log("Values did not match")

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
