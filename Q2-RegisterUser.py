import hashlib

# Mock database 
users_db = []

def hash_password(password):
    "Hash a password using SHA-256."
    return hashlib.sha256(password.encode()).hexdigest()

def email_exists(email):
    "Check if an email is already registered."
    return any(user["email"] == email for user in users_db)

def check_db_invariants():
    "Verify database invariants (should always hold true)."
    # 1. All emails must be unique
    emails = [user["email"] for user in users_db]
    assert len(emails) == len(set(emails)), "Invariant violated: Duplicate emails in database!"
    
    # 2. All passwords must be hashed (not plaintext)
    for user in users_db:
        assert len(user["password"]) == 64, "Invariant violated: Password not properly hashed!"  # SHA-256 produces 64-char hex
    
    # 3. All users must have 'email' and 'password' fields
    for user in users_db:
        assert "email" in user and "password" in user, "Invariant violated: Malformed user record!"

def register_user(email, password):
    
    assert email and password, "Pre-condition failed: Email and password must be provided."  
    assert "@" in email, "Pre-condition failed: Invalid email format."
    assert len(password) >= 8, "Pre-condition failed: Password must be at least 8 characters."
    assert not email_exists(email), "Pre-condition failed: Email is already registered."
    
    hashed_password = hash_password(password)
    new_user = {"email": email, "password": hashed_password}
    users_db.append(new_user)
    
    assert email_exists(email), "Post-condition failed: User was not added to the database."
    check_db_invariants() 
    
    print("\n=== REGISTRATION CONFIRMATION ===")
    print(f"User Email: {email}")
    print("Status: ACCOUNT CREATED")
    print("Database State:")
    for user in users_db:
        print(f" - {user['email']} (Password: {'*' * 8})")
    
    print("\n=== USER REGISTRATION COMPLETED ===")

register_user("group3@gmail.com", "Password123")
