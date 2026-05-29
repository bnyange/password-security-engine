# Password Security Engine

A Python-based tool that demonstrates why mathematically "strong" passwords still get cracked in seconds — and exactly how attackers do it. Built as a hands-on exploration of applied cryptography, Shannon entropy, and the time-memory tradeoff that underpins real-world credential attacks.

Interactive Streamlit dashboard lets you run all four engines live against any input.

---

## What this project covers

Most password security tools just tell you a password is "weak" or "strong." This project shows you *why*, by implementing both sides of the problem: the defensive math that measures password strength, and the offensive mechanics that bypass it.

The core insight is this: a password like `123456788` scores as mathematically moderate by Shannon entropy (it uses digits from a pool of 10, across 9 characters), but a pre-computed hash table cracks it in under a millisecond. The gap between mathematical complexity and human predictability is exactly what attackers exploit.

---

## Engines

### 1. Shannon entropy analyzer — `analyzer.py`

Calculates the information-theoretic entropy of a password using the formula `H = L × log₂(N)`, where `L` is password length and `N` is the character pool size (lowercase: 26, uppercase: 26, digits: 10, special characters: 32). Outputs an entropy score in bits, a 0–100 UI score normalised against 80 bits (considered exceptionally strong), and a qualitative label: Weak / Moderate / Strong.

### 2. Hash generator — `hasher.py`

Generates MD5, SHA-1, and SHA-256 hashes from a plaintext password, and demonstrates bcrypt salting. The contrast between fast, unsalted hashes and bcrypt is intentional — it's the same contrast that separates a leaked LinkedIn database from a properly engineered one.

### 3. Dictionary attack engine — `cracker.py`

Reads a wordlist line by line, hashes each candidate on the fly, and compares it against a target hash. The engine auto-detects the hash algorithm from string length (32 chars → MD5, 40 → SHA-1, 64 → SHA-256) without requiring manual configuration — demonstrating that attackers need very little information to begin cracking.

### 4. Pre-computed lookup table — `table.py` + `table_crack.py`

`table.py` reads a wordlist and pre-computes MD5, SHA-1, and SHA-256 hashes for every word, storing them in a JSON database (`rainbow.json`) as `hash → plaintext` mappings. `table_crack.py` then performs an O(1) dictionary lookup against that database — no hashing on the fly, no iteration. This is the time-memory tradeoff in practice: you pay the cost once at generation time, then crack any matching hash instantly.

---

## Architecture

```
password-security-engine/
├── app.py             # Streamlit dashboard — entry point
├── analyzer.py        # Shannon entropy calculation and strength scoring
├── hasher.py          # Hash generation (MD5, SHA-1, SHA-256, bcrypt)
├── cracker.py         # On-the-fly dictionary attack with auto algorithm detection
├── table.py           # Pre-computes hash→plaintext database from a wordlist
├── table_crack.py     # O(1) lookup attack against the pre-computed database
├── rainbow.json       # Pre-generated hash table (built from words.txt)
├── words.txt          # Wordlist used for cracking and table generation
└── .gitignore
```

---

## Setup

```bash
# Clone the repo
git clone https://github.com/bnyange/password-security-engine.git
cd password-security-engine

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows

# Install dependencies
pip install streamlit bcrypt

# Launch the dashboard
streamlit run app.py
```

To run individual engines from the terminal:

```bash
python analyzer.py          # entropy analysis
python cracker.py           # dictionary attack
python table.py             # generate a hash database
python table_crack.py       # O(1) lookup attack
```

---

## The time-memory tradeoff, demonstrated

| Attack method | Mechanism | Speed | Storage cost |
|---|---|---|---|
| Dictionary attack (`cracker.py`) | Hashes each word on the fly | O(n) — slower with large wordlists | Minimal |
| Table lookup (`table_crack.py`) | Pre-computed hash → plaintext map | O(1) — near-instant regardless of wordlist size | High (scales with wordlist) |

The tradeoff: the dictionary attack is cheap to set up but slow at runtime. The lookup table is expensive to generate once, but cracks any matching hash instantly thereafter. This is why salting defeats lookup tables — a unique salt per password means the attacker must recompute the entire table for every possible salt value.

---

## What I learned

- **Shannon entropy measures possibility space, not human behaviour.** A 9-digit password has 10⁹ possible values mathematically, but if it comes from a wordlist, it has exactly one. Entropy is a useful metric for random passwords; it's almost meaningless for passwords humans actually choose.

- **Hash algorithm identification requires no metadata.** The auto-detection in `cracker.py` — inferring MD5 vs SHA-1 vs SHA-256 purely from output length — mirrors what real cracking tools do. Attackers need the hash string and nothing else to begin.

- **Building the lookup table made bcrypt click.** When I generated `rainbow.json` and realised it could crack any matching MD5/SHA-1/SHA-256 hash instantly, the reason bcrypt uses salts became obvious: a unique salt per user means the table is useless. The same pre-computation that makes MD5 trivially crackable is exactly what bcrypt's cost factor prevents.

- **What I'd build next:** Add salt-aware cracking to demonstrate why even short unique salts defeat this approach. Add a comparison mode that runs both attack engines on the same hash and measures the time difference with a large wordlist.

---

## About `rainbow.json`

This file is the pre-computed hash database generated from `words.txt`. It contains MD5, SHA-1, and SHA-256 hashes mapped back to their plaintext equivalents. It is included in the repo for demonstration purposes — to show the output of `table.py` and enable `table_crack.py` to run without a generation step. No real user passwords or external data are included.

---

## Legal

Built and tested entirely using self-generated hashes and the bundled wordlist. All cracking demonstrations run against hashes I created myself. Do not use these tools against hashes or systems you do not own.

---

## Tech stack

- Python 3.11
- [Streamlit](https://streamlit.io/) — interactive dashboard
- [bcrypt](https://pypi.org/project/bcrypt/) — modern password hashing demonstration
- `hashlib` (stdlib) — MD5, SHA-1, SHA-256 generation and cracking
- `math`, `string` (stdlib) — Shannon entropy calculation
