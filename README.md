# CLI Encrypted Journal

A secure, terminal-based local journal application built entirely in **Python** using symmetric cryptographic architecture.

## Features
- **Key Derivation (PBKDF2):** Intentionally stretches passwords using 480,000 iterations of SHA-256 combined with a secure local unique salt to neutralize brute-force attacks.
- **Fernet Symmetric Encryption:** Encrypts user entries into unreadable byte blocks using the `cryptography` library.
- **Robust Access Controls:** Gracefully blocks access and denies text decryption if an invalid master key is entered.
- **Multi-line Inputs:** Supports typing long form journal entries natively inside the terminal environment.

## Requirements & Installation
Ensure you have Python installed, then install the cryptographic dependency:
```bash
pip install cryptography
```

## How to Run
```bash
python CLI_Encryption_Journal.py
```
