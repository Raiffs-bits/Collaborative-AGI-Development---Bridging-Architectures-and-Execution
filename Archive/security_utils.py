
# security_utils.py
# Encrypt/decrypt JSONL and trace files for secure storage

from cryptography.fernet import Fernet

def generate_key() -> bytes:
    return Fernet.generate_key()

def encrypt_file(key: bytes, infile: str, outfile: str):
    f = Fernet(key)
    with open(infile, 'rb') as fin:
        data = fin.read()
    enc = f.encrypt(data)
    with open(outfile, 'wb') as fout:
        fout.write(enc)

def decrypt_file(key: bytes, infile: str, outfile: str):
    f = Fernet(key)
    with open(infile, 'rb') as fin:
        data = fin.read()
    dec = f.decrypt(data)
    with open(outfile, 'wb') as fout:
        fout.write(dec)
