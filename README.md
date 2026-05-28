# 🔐 Cryptography & Password Security Engine

## Overview
This project is an interactive, Python-based educational tool designed to demonstrate the fundamental differences between mathematical password complexity and human predictability. It provides a full-lifecycle view of password security, featuring a defensive strength analyzer, a cryptographic hash generator, and two distinct offensive cracking engines.

The project highlights core computer science concepts, specifically the **Time-Memory Tradeoff**, by comparing on-the-fly dictionary attacks against $O(1)$ pre-computed hash table lookups.

## 🚀 Features

* **Defensive Analysis (Shannon Entropy):** Calculates the mathematical entropy of a password based on character pool size and length, providing a quantifiable security score.
* **Cryptographic Hash Generation:** Generates standard fast hashes (MD5, SHA-1, SHA-256) and demonstrates the security benefits of modern salting techniques using `bcrypt`.
* **Dynamic Dictionary Attack Engine:** An offensive script that reads wordlists, automatically detects the target hash algorithm based on string length (defensive programming), and attempts to crack the hash on the fly.
* **Pre-Computed Hash Table Lookup:** A demonstration of a "Rainbow Table" style attack. It pre-computes a massive JSON database of hashes, trading storage space to achieve near-instantaneous $O(1)$ cracking speeds.
* **Interactive UI:** A clean, responsive frontend built with Streamlit, allowing users to test inputs and execute attack sequences visually.

## 🧠 Core Concepts Demonstrated
* **Human Psychology vs. Mathematical Security:** Demonstrates why a mathematically "moderate" password (e.g., `123456788`) is instantly compromised by real-world attack vectors.
* **The Time-Memory Tradeoff:** Showcases the algorithmic efficiency difference between CPU-intensive on-the-fly hashing and storage-heavy pre-computed lookups.
* **Defensive Programming:** Implements auto-detection algorithms to handle user input gracefully without requiring manual configuration.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME

2. **Create and activate a virtual environment:**
Bash
On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

 On Windows
python -m venv .venv
.venv\Scripts\activate

3. **Install the required dependencies**
Bash
pip install streamlit bcrypt

4. **Launch the interactive visual dashboard**
streamlit run app.py
