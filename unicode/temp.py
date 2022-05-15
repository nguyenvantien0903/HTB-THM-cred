from Crypto.PublicKey import RSA
fp = open("keypair.pem", "r")
key = RSA.importKey(fp.read())
fp.close()
print("n:", hex(key.n))
print("e:", hex(key.e))