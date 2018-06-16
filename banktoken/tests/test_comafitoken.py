# Copyright (c) 2018 Nicolás Alvarez <nicolas.alvarez@gmail.com>
# Licensed under the GNU General Public License version 3 or any later version.
# See LICENSE.txt for details.

import unittest
from unittest.mock import patch, MagicMock
import base64

from .. import comafitoken

TEST_PAYLOAD = b'jNnbU15eXl5dMsxWZ5alkd9nFoWo1Eb1t0Izj4nh5PKVMGI0hOQLBQMv8k2t'
TEST_SEED = b'KGCQPVRVHCQgTLOeaSLGFTYQC'

class TestBankToken(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock(
            status_code=200,
            headers={'Content-Type': 'application/javascript'},
            content=b'callback(["%s"])' % TEST_PAYLOAD
        )

    @patch('banktoken.comafitoken.sess.get')
    def test_fetch(self, mock_get):
        '''Happy path fetching data'''
        mock_get.return_value = self.mock_response

        payload = comafitoken._fetch_encrypted_payload('99999999')

        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args[1]['params']['cupon'], '99999999')
        self.assertEqual(mock_get.call_args[1]['params']['callback'], 'callback')

        self.assertEqual(payload, base64.b64decode(TEST_PAYLOAD))

    def test_decrypt(self):
        '''Happy path decrypting data'''
        seed = comafitoken._decrypt_seed(base64.b64decode(TEST_PAYLOAD), '999999')

        self.assertEqual(seed, TEST_SEED)

    @patch('banktoken.comafitoken.sess.get')
    def test_all(self, mock_get):
        '''Happy path end to end'''

        mock_get.return_value = self.mock_response

        seed = comafitoken.activate('99999999', '999999')

        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args[1]['params']['cupon'], '99999999')
        self.assertEqual(mock_get.call_args[1]['params']['callback'], 'callback')

        self.assertEqual(seed, TEST_SEED)

if __name__ == '__main__':
    unittest.main()
