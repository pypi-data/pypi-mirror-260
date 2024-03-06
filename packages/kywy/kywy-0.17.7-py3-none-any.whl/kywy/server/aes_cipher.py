import base64
import codecs

from Crypto.Cipher import AES


class AesCipher(object):

    def __init__(self, key, iv):
        self.bs = AES.block_size
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def decrypt_script(encrypted_script: str,
                   aes_key):
    try:
        # The init vector is appended before the encrypted script (Length = 32)
        key_bytes = codecs.decode(aes_key, 'hex_codec')
        iv_bytes = codecs.decode(encrypted_script[:32], 'hex_codec')
        cipher = AesCipher(key=key_bytes, iv=iv_bytes)
        return cipher.decrypt(encrypted_script[32:])
    except Exception:
        # Decrypt fails:
        # Creates a script that raised a readable exception
        return 'raise Exception("Impossible to read the script, check the AES configuration")'
