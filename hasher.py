from hashlib import sha512
from string import ascii_lowercase, ascii_uppercase, digits
from getpass import getpass
from math import log
from argparse import ArgumentParser
from time import sleep
from contextlib import suppress

SYMBOLS = "!@#$%^&*"
CHARACTERS = ascii_lowercase + ascii_uppercase + digits + SYMBOLS

NOUNS1 = ['fire', 'queen', 'blog', 'tax', 'concrete', 'glove']
NOUNS2 = ['army', 'color', 'duck', 'morning', 'fear', 'train']
NOUNS3 = ['town', 'library', 'existence', 'pipe', 'instrument', 'army']

DEFAULT_LENGTH = 16
CODE_EXPOSURE = len(NOUNS1) * len(NOUNS2) * len(NOUNS3)

def escape(text):
	text = text.replace("\\", "\\\\")
	text = text.replace("|", "\\|")
	return text

def hash_components(password, username, domain):
	# hashes the password, salted with the username and domain
	# its not "safe", its intended to uniqify a master password
	components = []
	components.append(escape(password))
	components.append(escape(username))
	components.append(escape(domain.lower()))
	
	text = "|".join(components)
	return sha512(text.encode("utf-8")).digest()

def hash_to_pass(hash, size=DEFAULT_LENGTH):
	# takes a hash, and forms a `size`-char long password
	# there will be at least one lowercase, uppercase, digit, and symbol
	assert size <= log(2 ** (8 * len(hash)) // CODE_EXPOSURE, len(CHARACTERS)) # roughly 82

	value = int.from_bytes(hash, byteorder="little")
	value //= CODE_EXPOSURE

	result = []
	for _ in range(size):
		value, residue = divmod(value, len(CHARACTERS))
		result.append(CHARACTERS[residue])
	
	indices = list(range(size))
	for alphabet in (ascii_lowercase, ascii_uppercase, digits, SYMBOLS):
		value, index = divmod(value, len(indices))
		value, residue = divmod(value, len(alphabet))
		result[indices.pop(index)] = alphabet[residue]
	
	return "".join(result)

def hash_viz(password):
	# Emits 6**3 = 216 = ~7.75 bits of info, in 
	# the most distinguishable form possible, for typo recognition
	hash = sha512(password.encode("utf-8")).digest()
	value = int.from_bytes(hash, byteorder="little")

	words = []
	for alphabet in (NOUNS1, NOUNS2, NOUNS3):
		value, residue = divmod(value, len(alphabet))
		words.append(alphabet[residue])
	
	return " ".join(words).upper()

def print_banner():
	banner = r"""\
  _    _           _     _____
 | |  | |         | |   |  __ \
 | |__| | __ _ ___| |__ | |__) |_ _ ___ ___
 |  __  |/ _` / __| '_ \|  ___/ _` / __/ __|
 | |  | | (_| \__ \ | | | |  | (_| \__ \__ \
 |_|  |_|\__,_|___/_| |_|_|   \__,_|___/___/

 """
	print(banner)

def copy_to_clip(text):
	try:
		import pyperclip
		pyperclip.copy(text)
	except:
		return False
	return True

def prompt_interactive():
	print_banner()
	domain = input("Domain:\n> ")
	username = input("Username:\n> ")
	password = getpass("Password:\n> ")

	code_words = hash_viz(password)
	print("\nCode words: \"" + code_words + "\"")

	hash = hash_components(password, username, domain)
	hashpass = hash_to_pass(hash)
	print("HashPass: " + hashpass + "\n")

	if copy_to_clip(hashpass):
		print("HashPass copied to clipboard.")

	print("Exiting in 10 seconds.")
	sleep(10)
	

def prompt_silent():
	domain = input()
	username = input()
	password = getpass("")
		
	hash = hash_components(password, username, domain)
	hashpass = hash_to_pass(hash)

	print(hashpass)

def main():
	parser = ArgumentParser()
	parser.add_argument('-s', '--silent', action='store_true')
	args = parser.parse_args()

	try:
		if args.silent:
			prompt_silent()
		else:
			prompt_interactive()
	except KeyboardInterrupt:
		print("")


if __name__ == "__main__":
	main()
