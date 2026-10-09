import bcrypt

def hash_password(password: str) -> str:
    # 1. Convert the plain text string password to bytes using .encode('utf-8)
    password_bytes = password.encode('utf-8')
    # 2. Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    # 3. Hash the password with bcrypt.hashpw(password_bytes, salt)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # 4. Convert the resulting hashed byted back to a string with .decode('utf-8') and return it
    return hashed_bytes.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    # 1. Convert the plain text password attempt to bytes using .encode('utf-8')
    password_bytes = password.encode('utf-8')
    # 2. Convert the stored hash string back into bytes using .encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # 3. Use bcrypt.checkpw(password_bytes, hashed_bytes) to check if they match (True or False)
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Quick test block to run whe executing 'python3 auth.py directly:
if __name__ == "__main__":
    test_password = "my_secret_password123"

    # Step 1: Hash the password
    hashed = hash_password(test_password)
    print(f"Hashed password: {hashed}")

    # Step 2: Test Verification
    is_valid = verify_password("my_secret_password123", hashed)
    print(f"Password correct? {is_valid}")

    is_wrong = verify_password("wrong_password", hashed)
    print(f"Wrong password rejected? {not is_wrong}")