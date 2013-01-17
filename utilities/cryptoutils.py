# libraries
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256, HMAC

import os
if os.name != 'nt': 
	from Crypto import Random

class CryptoVariables:
	HASH_FUNCTION = SHA256
	SALT_SIZE = 8
	KEY_LENGTH = 64
	ITERATIONS = 1000

# PBKDF pseudo-random function. Used to mix a password and a salt.
# See Crypto\Protocol\KDF.py
pbkdf2_prf = lambda p, s: HMAC.new(p, s, CryptoVariables.HASH_FUNCTION).digest()

class CryptoUtil():
	@staticmethod
	def getKeyAndSalt(password):
		if os.name != 'nt': 
			salt = Random.get_random_bytes(CryptoVariables.SALT_SIZE)
		else:
			salt = os.urandom(CryptoVariables.SALT_SIZE)
		key = PBKDF2(password, salt, CryptoVariables.KEY_LENGTH, CryptoVariables.ITERATIONS, pbkdf2_prf)
		#hexsalt = ''.join('%02x' % ord(byte) for byte in salt)
		#hexkey = ''.join('%02x' % ord(byte) for byte in key)
		return { 'salt' : salt, 'key' : key }
                 
