import bcrypt

# password you want
password = "admin123"

# generate hash
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# print hash
print("Hashed Password:")
print(hashed.decode())