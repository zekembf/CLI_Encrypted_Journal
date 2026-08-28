import os 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
from cryptography.fernet import Fernet


# Define the file names we will use Locally.
JOURNAL_FILE = "journal.enc"
SALT_FILE = "salt.key"


def get_or_create_salt():

    """Generates a random 16-byte salt or loads an existing one."""

    if os.path.exists(SALT_FILE):

        # Open and read existing salt bytes
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:

        # Generate 16 bytes of cryptographically secure random data
        salt = os.urandom(16)

        # Save it locally for next time
        with open(SALT_FILE, "wb") as f:
            f.write(salt)

        print("🔑 Generated and saved a brand new salt key!")

        return salt

def generate_key(password: str, salt: bytes) -> bytes:
    """Derives a secure 32-byte cryptographic key from a plain password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # Deliberately slows down brute-force attacks
    )
    # Fernet requres the key to be URL-safe base64-encoded 32-byte key
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def add_entry(fernet: Fernet):
    """Encrypts and appends a new multi-line journal entry to the encrypted journal file."""
    print("\n--- Write your entry below (Press Enter then Ctrl+Z / Ctrl+D to finish and save) ---")

    # Capture mutliple lines of text until the user signals they are done (Ctrl+Z on Windows, Ctrl+D on Unix)
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break

    entry_text = "\n".join(lines)

    if not entry_text.strip():
        print("Empty Entry. Entry not saved.")
        return

    # Turn the string into raw bytes and encrypt it
    encrypted_entry = fernet.encrypt(entry_text.encode())

    # Save to file using 'ab' mode to append bytes
    with open(JOURNAL_FILE, "ab") as f:
        f.write(encrypted_entry + b"\n")  # Add a newline for separation
    print("\n Entry Successfully encrypted and saved to the journal!")

def read_entries(fernet: Fernet):
    """Reads, decrypts, and displays all saved journal entries. """
    if not os.path.exists(JOURNAL_FILE):
        print("\nYour journal is empty, no entries to display.")
        return

    print("\n--- Your Decrypted Journal Entries ---")
    try:
        with open(JOURNAL_FILE, "rb") as f:
            for line in f:
                line = line.strip()
                if line:
                    # Attempt to decrypt the binary line
                    decrypted_text = fernet.decrypt(line).decode()
                    print(f"\n {decrypted_text}")
                    print("-" * 40)
    except Exception:
        # If the key generated from the password is wrong, decryption fails automatically
        print("\nDecryption failed, the password you entered is incorrect.")

def main():
    print("Welcome to the Encrypted Journal CLI!")
    password = input("Please enter your password: ")

    # Initialise the security layers using Section 1 & 2 Logic.
    salt = get_or_create_salt()
    key = generate_key(password, salt)
    fernet = Fernet(key)
    print("Security layers initialized successfully!")

    while True:
        print("\n1. Write a new entry (WIP)")
        print("2. Read all entries (WIP)")
        print("3. Exit")
        choice = input("Please select an option (1-3): ")

        if choice == "1":
            add_entry(fernet)
        elif choice == "2":
            read_entries(fernet)
        elif choice == "3":
            print("Exiting the Encrypted Journal CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option. (1-3)")

if __name__ == "__main__":
    main()
