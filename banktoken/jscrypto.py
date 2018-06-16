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

__all__ = ['keyDerivation', 'aesCtrDecrypt']
