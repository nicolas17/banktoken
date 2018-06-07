# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.

'''
This module implements AES-CTR decryption compatible with the Javascript
implementation at http://www.movable-type.co.uk/scripts/aes.html.

aes.js is just an implementation of AES itself; it does nothing special.

aes-ctr.js has some non-standard things. The encryption function doesn't take
plaintext and key; rather it takes plaintext and a password, and it does its own
key derivation from the password. It also generates an IV (based on the current
time) and prepends it to the returned ciphertext. Key derivation is done by
using raw AES decryption with both key and plaintext set to the password (!).
Decryption works similarly: it takes ciphertext (with prepended IV) and password
(from which it derives the key in the same way as encryption).

This module implements CTR decryption in a way compatible with that Javascript
implementation. Encryption is not currently supported.
'''

import cryptography

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def keyDerivation(password, nBits):
    if nBits not in (128,192,256):
        raise ValueError()

    nBytes = nBits // 8

    pwBytes   = password.encode('utf8').ljust(nBytes, b'\0')
    pwBytes16 = password.encode('utf8').ljust(16, b'\0')

    cipher = Cipher(algorithms.AES(pwBytes), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    key = encryptor.update(pwBytes16)

    # expand key to 16/24/32 bytes long
    key += key[0:nBytes-16]

    return key

def aesCtrDecrypt(ciphertext, password, nBits):
    if nBits not in (128,192,256):
        raise ValueError()

    # recover nonce from 1st 8 bytes of ciphertext
    counterBlock = ciphertext[0:8]+b'\0'*8
    data = ciphertext[8:]

    cipher = Cipher(algorithms.AES(keyDerivation(password, nBits)), modes.CTR(counterBlock), backend=default_backend())
    encryptor = cipher.decryptor()
    return encryptor.update(ciphertext[8:])

if __name__ == '__main__':
    import base64
    import binascii

    # Examples from the JS library documentation
    assert keyDerivation('a',       128) == binascii.a2b_hex('60 84 dd 49 14 7b 5d 05 7a e3 f8 81 b9 0e e7 dd'.replace(' ',''))
    assert keyDerivation('b',       128) == binascii.a2b_hex('b4 1a 83 4f da 4b aa 41 76 62 be d6 2c 66 83 6d'.replace(' ',''))
    assert keyDerivation('\u263a',  128) == binascii.a2b_hex('d1 0c cd fd 44 45 54 ef 59 aa f8 dc 78 8e 9a 7c'.replace(' ',''))

    # Example from JS library comments
    assert aesCtrDecrypt(base64.b64decode('lwGl66VVwVObKIr6of8HVqJr'), 'p\u0101\u015f\u0161\u0175\u014d\u0159\u0111', 256) == b'big secret'

    # Test embedded in phone app
    assert aesCtrDecrypt(base64.b64decode('jNnbU15eXl5dMsxWZ5alkd9nFoWo1Eb1t0Izj4nh5PKVMGI0hOQLBQMv8k2t'), '999999', 256) == b'1426011923 KGCQPVRVHCQgTLOeaSLGFTYQC '

__all__ = ['keyDerivation', 'aesCtrDecrypt']
