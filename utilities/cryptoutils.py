# libraries
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256, HMAC

import os
if os.name != 'nt': 
	from Crypto import Random

class CryptoVariables:
	HASH_FUNCTION = SHA256
	SALT_SIZE = 8
	VERIFICATION_CODE_SIZE = 32
	SESSIONID_SIZE = 32
	PERSISTENT_TOKEN_SIZE = 32
	KEY_LENGTH = 64
	ITERATIONS = 1000

# PBKDF pseudo-random function. Used to mix a password and a salt.
pbkdf2_prf = lambda p, s: HMAC.new(p, s, CryptoVariables.HASH_FUNCTION).digest()

class CryptoUtil():
	@staticmethod
	def get_salt_and_key(password):
		'''
		Generates a random salt and a PBKDF2-based key for the given password and the random hash
		:param password:
		'''
		if os.name != 'nt': 
			salt = Random.get_random_bytes(CryptoVariables.SALT_SIZE)
		else:
			salt = os.urandom(CryptoVariables.SALT_SIZE)
		key = PBKDF2(password, salt, CryptoVariables.KEY_LENGTH, CryptoVariables.ITERATIONS, pbkdf2_prf)
		return salt, key

	@staticmethod
	def getKey(password, salt):
		key = PBKDF2(password, salt, CryptoVariables.KEY_LENGTH, CryptoVariables.ITERATIONS, pbkdf2_prf)
		return key

	@staticmethod
	def __get_random_bytes(size):
		if os.name != 'nt': 
			return Random.get_random_bytes(size)
		else:
			return os.urandom(size)

	@staticmethod
	def getVerificationCode():
		return CryptoUtil.__get_random_bytes(CryptoVariables.VERIFICATION_CODE_SIZE)

	@staticmethod
	def get_sessionId():
		return CryptoUtil.__get_random_bytes(CryptoVariables.SESSIONID_SIZE)
		
	@staticmethod
	def getPersistentId():
		return CryptoUtil.__get_random_bytes(CryptoVariables.PERSISTENT_TOKEN_SIZE)
		
