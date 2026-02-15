import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.config import CHAT_ENCRYPTION_KEY_V1

logger = logging.getLogger(__name__)

class EncryptionService:
    def __init__(self):
        if not CHAT_ENCRYPTION_KEY_V1:
            logger.error("CHAT_ENCRYPTION_KEY_V1 is not set in environment variables.")
            raise ValueError("CHAT_ENCRYPTION_KEY_V1 is required for encryption.")
        
        try:
            self.key = base64.b64decode(CHAT_ENCRYPTION_KEY_V1)
            if len(self.key) != 32:
                raise ValueError(f"Invalid key length: {len(self.key)} bytes. Must be 32 bytes.")
            self.aesgcm = AESGCM(self.key)
        except Exception as e:
            logger.error(f"Failed to initialize EncryptionService: {e}")
            raise

    def encrypt(self, plaintext: str) -> dict:
        """
        Encrypts plaintext using AES-256-GCM.
        Returns a dict with encrypted_content (base64 encoded), version, and is_encrypted flag.
        Encrypted content structure: IV (12 bytes) + Ciphertext + Tag
        """
        try:
            iv = os.urandom(12)
            # AESGCM.encrypt in cryptography handles the auth tag automatically (concatenates it)
            ciphertext_with_tag = self.aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)
            
            # Concatenate IV + Ciphertext (which includes Tag)
            combined = iv + ciphertext_with_tag
            
            return {
                "encrypted_content": combined,
                "encryption_version": 1,
                "is_encrypted": True
            }
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, combined_data: bytes) -> str:
        """
        Decrypts combined data (IV + Ciphertext + Tag).
        """
        try:
            if len(combined_data) < 12:
                raise ValueError("Invalid encrypted data length.")
            
            iv = combined_data[:12]
            ciphertext_with_tag = combined_data[12:]
            
            plaintext_bytes = self.aesgcm.decrypt(iv, ciphertext_with_tag, None)
            return plaintext_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Failed to decrypt message. It might be corrupted or the key might be incorrect.")

# Singleton instance
encryption_service = EncryptionService()
