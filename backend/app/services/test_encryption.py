import os
import base64
from app.services.encryption import EncryptionService

def test_encryption_roundtrip():
    # Setup service with a temporary key
    test_key = base64.b64encode(os.urandom(32)).decode()
    os.environ["CHAT_ENCRYPTION_KEY_V1"] = test_key
    
    # Re-initialize service for this test
    service = EncryptionService()
    
    plaintext = "Hello, this is a secret legal message!"
    result = service.encrypt(plaintext)
    
    assert result["is_encrypted"] is True
    assert result["encryption_version"] == 1
    assert isinstance(result["encrypted_content"], bytes)
    
    decrypted = service.decrypt(result["encrypted_content"])
    assert decrypted == plaintext
    print("✓ Encryption roundtrip test passed!")

def test_decryption_failure():
    test_key = base64.b64encode(os.urandom(32)).decode()
    os.environ["CHAT_ENCRYPTION_KEY_V1"] = test_key
    service = EncryptionService()
    
    # Invalid data
    try:
        service.decrypt(b"invalid_data_too_short")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Failed to decrypt message" in str(e)
    
    # Wrong data but long enough
    try:
        service.decrypt(os.urandom(50))
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Failed to decrypt message" in str(e)
    print("✓ Decryption failure test passed!")

if __name__ == "__main__":
    test_encryption_roundtrip()
    test_decryption_failure()
    print("\nAll encryption tests passed!")
