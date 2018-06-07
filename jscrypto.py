# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.

import cryptography
import base64

data = base64.b64decode("jNnbU15eXl5dMsxWZ5alkd9nFoWo1Eb1t0Izj4nh5PKVMGI0hOQLBQMv8k2t")
password = '999999'
nBits = 256

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def dumbKeyDerivation(password, nBits):
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

def dumbAesCtrDecrypt(ciphertext, password, nBits):
    if nBits not in (128,192,256):
        raise ValueError()

    # recover nonce from 1st 8 bytes of ciphertext
    counterBlock = ciphertext[0:8]+b'\0'*8
    data = ciphertext[8:]

    cipher = Cipher(algorithms.AES(dumbKeyDerivation(password, nBits)), modes.CTR(counterBlock), backend=default_backend())
    encryptor = cipher.decryptor()
    return encryptor.update(ciphertext[8:])

print(dumbAesCtrDecrypt(data, password, nBits))
