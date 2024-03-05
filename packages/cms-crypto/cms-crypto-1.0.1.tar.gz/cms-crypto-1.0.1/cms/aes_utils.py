import base64
from Crypto.Cipher import AES

BS = 16
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def aes_decrypt(value, iv, key):
    # Converting iv and key into byte string, else it will throw error
    iv = iv.encode('utf-8')
    key = key.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(base64.b64decode(value)).decode())


def base64_decrypt(value):
    return base64.b64decode(value).decode()


def decrypt(value, typ: str, iv, key):
    if typ.upper() == 'AES':
        return aes_decrypt(value, iv, key)
    elif typ.upper() == 'BASE64':
        return base64_decrypt(value)
    else:
        raise Exception('Invalid encryption type!')
