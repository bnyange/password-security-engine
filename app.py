import streamlit as st
import math
import string
import hashlib
import time
import json
import os

# --- 1. Core Logic Functions ---
def evaluate_strength(password):
    if not password: return 0, "None", 0
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26
    if any(c.isupper() for c in password): pool_size += 26
    if any(c.isdigit() for c in password): pool_size += 10
    if any(c in string.punctuation for c in password): pool_size += 32
    
    entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
    score = min(int((entropy / 80) * 100), 100)
    
    if entropy < 28: label = "Weak"
    elif entropy < 50: label = "Moderate"
    else: label = "Strong"
    return score, label, entropy

def hash_word(word, algorithm="md5"):
    encoded = word.encode('utf-8')
    if algorithm == "md5": return hashlib.md5(encoded).hexdigest()
    if algorithm == "sha256": return hashlib.sha256(encoded).hexdigest()

def dictionary_attack(target_hash, wordlist_path, ui_progress_bar=None):
    start_time = time.time()
    try:
        # Get total file size to calculate progress accurately
        file_size = os.path.getsize(wordlist_path)
        bytes_read = 0

        # errors='ignore' is crucial here because rockyou.txt has some corrupted characters
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for attempts, line in enumerate(f, 1):
                # Track how much of the file we have read
                bytes_read += len(line.encode('utf-8', errors='ignore'))
                
                # Update the UI every 500,000 lines to prevent browser freezing
                if ui_progress_bar and attempts % 500000 == 0:
                    progress_pct = min(bytes_read / file_size, 1.0)
                    ui_progress_bar.progress(progress_pct, text=f"Scanned {attempts:,} passwords...")

                guess = line.strip()
                if hash_word(guess, "md5") == target_hash or hash_word(guess, "sha256") == target_hash:
                    if ui_progress_bar: ui_progress_bar.progress(1.0, text="Match Found!")
                    return guess, time.time() - start_time
                    
    except FileNotFoundError:
        pass
    return None, time.time() - start_time

def table_attack(target_hash, db_path):
    start_time = time.time()
    try:
        with open(db_path, 'r') as f:
            database = json.load(f)
            if target_hash in database:
                return database[target_hash], time.time() - start_time
    except FileNotFoundError:
        pass
    return None, time.time() - start_time

# --- 2. Streamlit UI Layout ---
st.set_page_config(page_title="Cybersec Portfolio", layout="centered")

st.title("🔐 Cryptography & Password Engine")
st.markdown("An educational demonstration of password entropy vs. cryptographic vulnerabilities.")

# User Input
password_input = st.text_input("Enter a password to analyze and attack:", type="password")

if password_input:
    st.divider()
    
    # --- Defense: Analysis ---
    st.subheader("🛡️ Defensive Analysis")
    score, label, entropy = evaluate_strength(password_input)
    
    col1, col2 = st.columns(2)
    col1.metric("Shannon Entropy", f"{entropy:.2f} bits")
    col2.metric("Strength Rating", label)
    st.progress(score / 100, text=f"Security Score: {score}/100")

    # --- Cryptography: Hashing ---
    st.subheader("⚙️ Hash Generation")
    md5_target = hash_word(password_input, "md5")
    sha256_target = hash_word(password_input, "sha256")
    st.code(f"MD5: {md5_target}\nSHA-256: {sha256_target}")

    # --- Offense: Cracking ---
    st.subheader("🥷 Offensive Cracking Engine")
    
    # Let the user choose their dictionary
    dict_choice = st.radio("Select Dictionary Size:", ["Fast Test (words.txt - 50 words)", "Deep Scan (rockyou.txt - 14.3 Million words)"])
    selected_file = "words.txt" if "Fast Test" in dict_choice else "rockyou.txt"

    if st.button("Initiate Attack Sequence", type="primary"):
        
        # Create an empty placeholder for our progress bar
        st.markdown(f"**Target:** `{md5_target}`")
        my_bar = st.progress(0, text="Initializing dictionary attack...")
        
        # Run Dictionary Attack and pass the progress bar into the function
        dict_result, dict_time = dictionary_attack(md5_target, selected_file, ui_progress_bar=my_bar)
        
        # Run Table Attack (No progress bar needed because it's instant)
        table_result, table_time = table_attack(md5_target, "rainbow.json")
        
        # Display Results
        st.divider()
        if dict_result:
            st.success(f"**Dictionary Attack Successful!** Password '{dict_result}' cracked in {dict_time:.4f} seconds.")
        else:
            st.error(f"Dictionary Attack Failed: Password not found in {selected_file}.")
            
        if table_result:
            st.success(f"**Rainbow Table Lookup Successful!** Password '{table_result}' found in {table_time:.8f} seconds.")
        else:
            st.error("Table Attack Failed: Hash not in rainbow.json")