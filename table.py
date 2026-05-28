import hashlib
import json
import time

def generate_lookup_table(wordlist_path, output_json_path):
    """Reads a wordlist, computes hashes, and saves them to a JSON database."""
    print(f"[*] Generating Pre-computed Hash Tables from '{wordlist_path}'...")
    start_time = time.time()
    
    # The dictionary that will hold our database
    database = {}
    word_count = 0

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word = line.strip()
                encoded_word = word.encode('utf-8')
                
                # Compute all three hashes so our table is robust
                md5_hash = hashlib.md5(encoded_word).hexdigest()
                sha1_hash = hashlib.sha1(encoded_word).hexdigest()
                sha256_hash = hashlib.sha256(encoded_word).hexdigest()
                
                # Map the hash back to the plaintext word
                database[md5_hash] = word
                database[sha1_hash] = word
                database[sha256_hash] = word
                
                word_count += 1

        # Save the database to a JSON file
        with open(output_json_path, 'w') as json_file:
            json.dump(database, json_file, indent=4)
            
        end_time = time.time()
        print(f"[+] Success! Mapped {word_count} words into {word_count * 3} hashes.")
        print(f"[+] Database saved to '{output_json_path}'")
        print(f"[+] Time taken: {end_time - start_time:.4f} seconds")

    except FileNotFoundError:
        print(f"[-] Error: Could not find '{wordlist_path}'.")

if __name__ == "__main__":
    print("--- Database Generator ---")
    wordlist = input("Enter your wordlist filename (e.g., words.txt): ").strip()
    output_name = input("Enter the output database name (e.g., rainbow.json): ").strip()
    
    generate_lookup_table(wordlist, output_name)