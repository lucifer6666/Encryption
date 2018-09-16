import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import hashlib
import getpass


def encrypt(key, filename):
	chunksize=64*1024
	outputfile= "encrypted_"+filename
	filesize=str(os.path.getsize(filename)).zfill(16)
	IV= Random.new().read(AES.block_size)

	

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open (filename, 'rb') as infile :
		with open (outputfile, 'wb') as outfile :
			outfile.write(filesize.encode())
			outfile.write(IV)

			while True:
				chunk=infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' *(16 - (len(chunk) % 16))


				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize=64*1024
	outputfile=filename[10:]

	with open (filename, 'rb') as infile:
		filesize=int(infile.read(16))
		IV=infile.read(16)
		decryptor=AES.new(key, AES.MODE_CBC, IV)

		with open (outputfile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

def getkey(password):

	hasher = hashlib.sha256(password.encode())
	return hasher.digest()

def main():
	choice = input("(E)ncrypt or (D)ecrypt ? :")


	if choice == 'E':
		filename=input("File to Encrypt:")
		password=input("Password :")
		encrypt(getkey(password), filename)
		print("Done.")

	elif choice == 'D':
		filename=input("File to Decrypt:")
		password=input("Password :")
		decrypt(getkey(password), filename)
		print("Done.")

	else:
		print("No Option Selected....")

if __name__ == '__main__':
	main()