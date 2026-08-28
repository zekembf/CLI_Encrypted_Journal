import os 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

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

# A quick test to ensure the salt is generated and saved correctly
if __name__ == "__main__":
    print("--- Testing Section 1 ---")
    my_salt = get_or_create_salt()
    print(f"Your salt key bytes: {my_salt}")


