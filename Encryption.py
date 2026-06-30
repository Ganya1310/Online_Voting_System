from cryptography.fernet import Fernet

# 🔐 Paste your key here
key = b'JYjeB_ZBI6kSeRGDxwp2XvBqNUPnUdC_r0PSAaSEYqE='

cipher = Fernet(key)

def encrypt_vote(vote):
    return cipher.encrypt(vote.encode()).decode()

def decrypt_vote(encrypted_vote):
    return cipher.decrypt(encrypted_vote.encode()).decode()