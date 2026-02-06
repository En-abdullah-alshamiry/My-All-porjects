




# باختصار، كيف يعملون معاً؟
# Padding: يجهز مقاس البيانات (يكمل النص الناقص).

# Algorithms: يختار نوع القفل (AES مثلاً).

# Modes: يقرر كيف يربط السلاسل (CBC).

# Backend: يوفر الرياضيات اللازمة.

# Cipher: يجمعهم كلهم في أمر واحد ليبدأ التشفير.





import base64
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pad_data(data):
    padder = padding.PKCS7(64).padder() # DES/3DES block size is 64 bits
    if isinstance(data, str):
        data = data.encode()
    return padder.update(data) + padder.finalize()

def unpad_data(data):
    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def aes_encrypt(text, key): 
    # AES key must be 16, 24, or 32 bytes
    key_bytes = key.encode().ljust(32, b'\0')[:32]
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return IV + Ciphertext encoded in base64
    return base64.b64encode(iv + ct).decode()

def aes_decrypt(ciphertext, key):
    raw_data = base64.b64decode(ciphertext)
    iv = raw_data[:16]
    ct = raw_data[16:]
    
    key_bytes = key.encode().ljust(32, b'\0')[:32]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    pt_padded = decryptor.update(ct) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    pt = unpadder.update(pt_padded) + unpadder.finalize()
    return pt.decode()

def triple_des_encrypt(text, key):
    # 3DES key must be 16 or 24 bytes
    key_bytes = key.encode().ljust(24, b'\0')[:24]
    iv = os.urandom(8)
    
    padded_data = pad_data(text)
    
    cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    
    return base64.b64encode(iv + ct).decode()

def triple_des_decrypt(ciphertext, key):
    raw_data = base64.b64decode(ciphertext)
    iv = raw_data[:8]
    ct = raw_data[8:]
    
    key_bytes = key.encode().ljust(24, b'\0')[:24]
    cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    pt_padded = decryptor.update(ct) + decryptor.finalize()
    pt = unpad_data(pt_padded)
    return pt.decode()

# Note: 'cryptography' library doesn't support plain DES (it's insecure).
# We will use TripleDES with a repeated key as a fallback for the DES request 
# or inform the user.
def des_encrypt(text, key):
    # Emulating DES using TripleDES (K1=K2=K3) for demonstration
    key_bytes = key.encode().ljust(8, b'\0')[:8]
    # TripleDES with same 8 bytes repeated 3 times is effectively DES
    full_key = key_bytes * 3 
    return triple_des_encrypt(text, full_key.decode('latin-1'))

def des_decrypt(ciphertext, key):
    key_bytes = key.encode().ljust(8, b'\0')[:8]
    full_key = key_bytes * 3
    return triple_des_decrypt(ciphertext, full_key.decode('latin-1'))
