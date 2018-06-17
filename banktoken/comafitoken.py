# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.


import time
import re
import base64

import requests

from . import jscrypto

sess = requests.session()

def fetch_encrypted_payload(activation_code):
    r = sess.get(
        "https://tokenv.banelcoservices.com.ar/vuserver/activation.php",
        params={
            'cupon': activation_code,
            'callback': 'callback',
            '_': str(int(time.time() * 1000))
        }
    )

    if r.status_code != 200:
        raise RuntimeError("status_code not 200") # FIXME better exception

    content_type = r.headers.get('Content-Type', '')
    if content_type == 'application/javascript':
        m = re.fullmatch(rb'callback\(\["(.*)"\]\)', r.content)
        if m is None:
            raise RuntimeError("raw response has unexpected format")

        b64_data = m.group(1).replace(br'\/', b'/')

        encrypted_blob = base64.b64decode(b64_data)
        return encrypted_blob

    elif content_type == 'text/html':
        if r.content == b'URL Incorrecta - contacte Soporte Security':
            raise RuntimeError("Got 'incorrect url' error - bad token?")
        else:
            raise RuntimeError("Got unknown error")
    else:
        raise RuntimeError("Got unexpected content type")

def decrypt_seed(payload, passcode):
    decrypted_payload = jscrypto.aesCtrDecrypt(payload, passcode, 256)

    m = re.fullmatch(rb'([0-9]+) ([0-9a-zA-Z=]+) ([01]?)', decrypted_payload)
    if m is None:
        # likely decryption failed because the passcode is wrong
        raise RuntimeError("Decryption gave wrong format")

    crc, seed, forcePasscodeReset = m.groups()
    # TODO verify CRC
    return seed

def activate(activation_code, passcode):

    encrypted_blob = fetch_encrypted_payload(activation_code)
    return decrypt_seed(encrypted_blob, passcode)

