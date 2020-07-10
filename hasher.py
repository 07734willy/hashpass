from hashlib import sha512
from string import ascii_lowercase, ascii_uppercase, digits
from getpass import getpass

symbols = "!@#$%^&*"
characters = ascii_lowercase + ascii_uppercase + digits + symbols

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
	components.append(escape(domain))
	
	text = "|".join(components)
	return sha512(text.encode("utf-8")).digest()

def hash_to_pass(hash, size):
	# takes a hash, and forms a `size`-char long password
	# there will be at least one lowercase, uppercase, digit, and symbol
	assert size <= 56

	value = int.from_bytes(hash, byteorder="little")

	result = []
	for _ in range(size):
		value, residue = divmod(value, len(characters))
		result.append(characters[residue])
	
	indices = list(range(size))
	for alphabet in (ascii_lowercase, ascii_uppercase, digits, symbols):
		value, index = divmod(value, len(indices))
		value, residue = divmod(value, len(alphabet))
		result[indices.pop(index)] = alphabet[residue]
	
	return "".join(result)

def hash_viz(password):
	# Emits 6**3 = 216 = ~7.75 bits of info, in 
	# the most distinguishable form possible, for typo recognition
	hash = sha512(password.encode("utf-8")).digest()
	value = int.from_bytes(hash, byteorder="little")

	nouns1 = ['fire', 'queen', 'blog', 'tax', 'concrete', 'glove']
	nouns2 = ['army', 'color', 'duck', 'morning', 'fear', 'train']
	nouns3 = ['town', 'library', 'existence', 'pipe', 'instrument', 'army']

	words = []
	for alphabet in (nouns1, nouns2, nouns3):
		value, residue = divmod(value, len(alphabet))
		words.append(alphabet[residue])
	
	return " ".join(words)

def print_banner():
	banner = r"""
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

def main():
	print_banner()
	domain = input("Domain:\n> ").lower()
	username = input("Username:\n> ")
	password = getpass("Password:\n> ")

	code_words = hash_viz(password)
	print("\nCode words: \"" + code_words + "\"")

	hash = hash_components(password, username, domain)
	hashpass = hash_to_pass(hash, 16)
	print("HashPass: " + hashpass + "\n")

	if copy_to_clip(hashpass):
		input("HashPass copied to clipboard. Press any key to exit.")
	else:
		input("Once you have copied the HashPass, press any key to exit.")

if __name__ == "__main__":
	main()
