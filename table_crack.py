import json
import time

def identify_algorithm(target_hash):
    """Auto-detects the hash algorithm based on string length."""
    length = len(target_hash)
    if length == 32: return "MD5"
    elif length == 40: return "SHA-1"
    elif length == 64: return "SHA-256"
    else: return "Unknown"

def table_attack(target_hash, database_path):
    """Cracks a hash by looking it up in a pre-computed JSON database."""
    algorithm = identify_algorithm(target_hash)
    
    if algorithm == "Unknown":
        print(f"[-] Error: Unrecognized hash length ({len(target_hash)} chars).")
        return None

    print(f"\n[*] Target identified as {algorithm}...")
    print(f"[*] Loading massive database into memory...")
    
    try:
        # Load the pre-computed hashes into memory
        with open(database_path, 'r') as file:
            database = json.load(file)
            
        print(f"[*] Executing $O(1)$ table lookup...")
        start_time = time.time()
        
        # The actual "attack" is just a simple Python dictionary lookup
        target_lower = target_hash.lower()
        if target_lower in database:
            end_time = time.time()
            plaintext = database[target_lower]
            print(f"\n[+] SUCCESS! Hash cracked instantly!")
            print(f"[+] Password     : '{plaintext}'")
            print(f"[+] Time taken   : {end_time - start_time:.8f} seconds")
            return plaintext
        else:
            print("\n[-] FAILED. Hash not found in the pre-computed table.")
            return None

    except FileNotFoundError:
        print(f"[-] Error: Could not find the database at '{database_path}'.")

if __name__ == "__main__":
    print("--- Pre-computed Table Cracker ---")
    target = input("Enter the target hash to crack: ").strip()
    db_file = input("Enter your database filename (e.g., rainbow.json): ").strip()
    
    table_attack(target, db_file)