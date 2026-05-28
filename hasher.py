import hashlib
import bcrypt

def generate_fast_hashes(password):
    # Hashlib requires the string to be encoded into bytes before hashing
    encoded_pw = password.encode('utf-8')
    
    md5_hash = hashlib.md5(encoded_pw).hexdigest()
    sha1_hash = hashlib.sha1(encoded_pw).hexdigest()
    sha256_hash = hashlib.sha256(encoded_pw).hexdigest()
    
    return md5_hash, sha1_hash, sha256_hash

def generate_secure_bcrypt(password):
    """Generates a salted bcrypt hash."""
    encoded_pw = password.encode('utf-8')
    
    # This completely neutralizes pre-computed rainbow table attacks.
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded_pw, salt)
    
    # Decode back to string for clean terminal output
    return hashed.decode('utf-8') 


if __name__ == "__main__":
    print("--- Password Hash Generator ---")
    test_password = input("Enter a password to hash: ")
    
    md5, sha1, sha256 = generate_fast_hashes(test_password)
    
    print(f"\nHashes for '{test_password}':")
    print(f"MD5     : {md5}")
    print(f"SHA-1   : {sha1}")
    print(f"SHA-256 : {sha256}")
    
    # Run bcrypt twice to demonstrate salting
    print("\n--- Bcrypt Demonstration ---")
    print(f"Bcrypt 1: {generate_secure_bcrypt(test_password)}")
    print(f"Bcrypt 2: {generate_secure_bcrypt(test_password)}")