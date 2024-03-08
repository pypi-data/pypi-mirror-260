import base64
import bcrypt
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from injectable import injectable


@injectable
class UtilsCryptography:
    # Hash a password with bcrypt
    def bcrypt_hash(self, password_raw: str) -> str:
        return bcrypt.hashpw(password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Check is the hashed password matches with bcrypt
    def bcrypt_check(self, password_raw: str, password_hashed: str) -> bool:
        return bcrypt.checkpw(password=password_raw.encode('utf-8'), hashed_password=password_hashed.encode('utf-8'))
    
    def _aes_pad(self, s: str) -> str:
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    
    def _aes_unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
    
    def aes_encrypt(self, text_raw: str, password: str) -> str:
        # Build key and IV
        password_bytes = password.encode("utf-8")
        private_key_bytes = hashlib.sha256(password_bytes).digest()
        iv_bytes = Random.new().read(AES.block_size)

        # Build cipher
        cipher = AES.new(private_key_bytes, AES.MODE_CBC, iv_bytes)

        # Build text
        text_padded_raw = self._aes_pad(text_raw)
        text_padded_bytes = text_padded_raw.encode("utf-8")

        # Encrypt and return
        encrypted_bytes = iv_bytes + cipher.encrypt(text_padded_bytes)
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def aes_decrypt(self, text_encrypted: str, password: str) -> str:
        # Get encrypted bytes
        encrypted_bytes = base64.b64decode(text_encrypted)

        # Build key and IV
        password_bytes = password.encode("utf-8")
        private_key_bytes = hashlib.sha256(password_bytes).digest()
        iv_bytes = encrypted_bytes[:AES.block_size]

        # Build cipher
        cipher = AES.new(private_key_bytes, AES.MODE_CBC, iv_bytes)

        # Decrypt
        text_padded_bytes = cipher.decrypt(encrypted_bytes[AES.block_size:])
        text_bytes = self._aes_unpad(text_padded_bytes)
        return text_bytes.decode("utf-8")
