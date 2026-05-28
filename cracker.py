import hashlib
import time

def identify_algorithm(target_hash):
    """Auto-detects the hash algorithm based on string length."""
    length = len(target_hash)
    
    if length == 32:
        return "md5"
    elif length == 40:
        return "sha1"
    elif length == 64:
        return "sha256"
    else:
        return None

def hash_word(word, algorithm):
    """Hashes a single word using the specified algorithm."""
    encoded_word = word.encode('utf-8')
    
    if algorithm == "md5":
        return hashlib.md5(encoded_word).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(encoded_word).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(encoded_word).hexdigest()

def dictionary_attack(target_hash, wordlist_path):
    """Attempts to crack a hash by guessing words from a dictionary."""
    
    # 1. Auto-detect the algorithm
    algorithm = identify_algorithm(target_hash)
    
    if not algorithm:
        print(f"[-] Error: Unrecognized hash length ({len(target_hash)} chars). This tool supports MD5, SHA-1, and SHA-256.")
        return None

    print(f"\n[*] Target identified as {algorithm.upper()}...")
    print(f"[*] Starting dictionary attack...")
  
    attempts = 0

    try:
        # 2. Execute the attack
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                attempts += 1
                guess = line.strip()
                
                guess_hash = hash_word(guess, algorithm)
                
                # Compare it to the target
                if guess_hash == target_hash.lower():
                 
                    print(f"\n[+] SUCCESS! Hash cracked!")
                    print(f"[+] Password     : '{guess}'")
                    print(f"[+] Attempts     : {attempts}")
                    return guess

        print("\n[-] FAILED. Password not found in the dictionary.")
        return None

    except FileNotFoundError:
        print(f"[-] Error: Could not find the wordlist file at '{wordlist_path}'.")
        return None

# --- Testing the Code ---
if __name__ == "__main__":
    print("--- Auto-Detecting Dictionary Cracker ---")
    
    # We only need to ask for the hash and the wordlist now!
    target = input("Enter the target hash to crack: ").strip()
    wordlist = input("Enter the filename of your wordlist (e.g., words.txt): ").strip()
    
    dictionary_attack(target, wordlist)