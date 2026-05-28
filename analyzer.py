import math
import string

def calculate_entropy(password):
    """Calculates the Shannon entropy of a given password."""
    if not password:
        return 0

    pool_size = 0
    
    # Determine the pool size based on character types present
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += 32  # Standard special characters

    # If the pool size is still 0 (e.g., non-standard characters only), avoid math errors
    if pool_size == 0:
        return 0

    # Calculate Entropy: Length * log2(Pool Size)
    entropy = len(password) * math.log2(pool_size)
    return entropy

def evaluate_strength(password):
    """Returns a score (0-100) and a qualitative strength label."""
    entropy = calculate_entropy(password)

    # Categorize based on standard entropy bit strengths
    if entropy < 28:
        strength = "Weak"
    elif entropy < 50:
        strength = "Moderate"
    else:
        strength = "Strong"

    # Normalize the entropy to a 0-100 score for our future UI progress bar
    # 80 bits is generally considered exceptionally strong, so we cap the score there
    score = min(int((entropy / 80) * 100), 100)

    return score, strength, entropy

# --- Testing the Code ---
if __name__ == "__main__":
    print("--- Password Strength Analyzer ---")
    test_password = input("Enter a password to test: ")
    
    score, label, ent = evaluate_strength(test_password)
    
    print(f"\nResults for '{test_password}':")
    print(f"Calculated Entropy : {ent:.2f} bits")
    print(f"UI Score           : {score}/100")
    print(f"Strength Label     : {label}")