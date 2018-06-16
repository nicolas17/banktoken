# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.

import unittest

import base64
import binascii

from .. import jscrypto

class TestJSCrypto(unittest.TestCase):
    def test_key_derivation(self):
        # Examples from the JS library documentation
        self.assertEqual(jscrypto.keyDerivation('a',      128), binascii.a2b_hex('60 84 dd 49 14 7b 5d 05 7a e3 f8 81 b9 0e e7 dd'.replace(' ','')))
        self.assertEqual(jscrypto.keyDerivation('b',      128), binascii.a2b_hex('b4 1a 83 4f da 4b aa 41 76 62 be d6 2c 66 83 6d'.replace(' ','')))
        self.assertEqual(jscrypto.keyDerivation('\u263a', 128), binascii.a2b_hex('d1 0c cd fd 44 45 54 ef 59 aa f8 dc 78 8e 9a 7c'.replace(' ','')))

    def test_decrypt_unicodepw(self):
        # Example from JS library comments
        self.assertEqual(jscrypto.aesCtrDecrypt(base64.b64decode('lwGl66VVwVObKIr6of8HVqJr'), 'p\u0101\u015f\u0161\u0175\u014d\u0159\u0111', 256), b'big secret')

    def test_decrypt(self):
        # Test embedded in phone app
        self.assertEqual(jscrypto.aesCtrDecrypt(base64.b64decode('jNnbU15eXl5dMsxWZ5alkd9nFoWo1Eb1t0Izj4nh5PKVMGI0hOQLBQMv8k2t'), '999999', 256), b'1426011923 KGCQPVRVHCQgTLOeaSLGFTYQC ')

if __name__ == '__main__':
    unittest.main()
