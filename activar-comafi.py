#!/usr/bin/python3

# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.

import sys
import re
import base64

from banktoken import comafitoken
import pyqrcode

comafitoken.sess.verify = False

activation_code = input("Ingresá el código de asociación que figura en el ticket (8 caracteres): ")
activation_code = activation_code.strip()

print("Contactando servidor...", end='')
sys.stdout.flush()
encrypted_blob = comafitoken.fetch_encrypted_payload(activation_code)
print()

did_decrypt = False
while not did_decrypt:
    passcode = input("Ingresá la clave que generaste en el cajero (6 dígitos): ").strip()
    if not re.match('^[0-9]{6}$', passcode):
        print("La clave debe tener 6 dígitos\n")
        continue

    try:
        seed = comafitoken.decrypt_seed(encrypted_blob, passcode)
        did_decrypt = True
    except RuntimeError as e:
        print("Clave incorrecta\n")
        continue

print()
print("Activación correcta")

seed_b32 = base64.b32encode(seed)
url = 'otpauth://totp/Comafi%%20Token?secret=%s&issuer=Comafi&period=40' % seed_b32.decode('latin1')

qr = pyqrcode.create(url, error='L')
print(qr.terminal())

print("URL: %s" % url)
print()
print("Para activación manual:")
print("    Clave plana: %s" % seed.decode('latin1'))
print("    Clave Base32: %s" % seed_b32.decode('latin1'))
print("    Período: 40 segundos")
