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
            print("Write a new entry functionality is a work in progress.")
        elif choice == "2":
            print("Read all entries functionality is a work in progress.")
        elif choice == "3":
            print("Exiting the Encrypted Journal CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option. (1-3)")

if __name__ == "__main__":
    main()
