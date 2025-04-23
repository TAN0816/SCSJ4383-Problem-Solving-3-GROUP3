import hashlib

# ========================
# Class/Module: RegisterUser
# ========================
class RegisterUser:
    def __init__(self):
        self.users = []  # Simulated user database

    def is_email_unique(self, email):
        return all(user["email"] != email for user in self.users)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, email, password):
        # === Pre-condition ===
        # Email and password must be provided and valid
        assert email and "@" in email, "Email must be in a valid format"
        assert len(password) >= 8, "Password must be at least 8 characters long"
        assert self.is_email_unique(email), "Email is already registered"

        # === Process ===
        # Hash the password and store the user
        hashed_pw = self.hash_password(password)
        self.users.append({"email": email, "password": hashed_pw})

        # === Post-condition ===
        # The new user must be present in the list
        assert any(u["email"] == email for u in self.users), "User was not added"

        # === Invariant ===
        # All emails in the database must be unique
        emails = [u["email"] for u in self.users]
        assert len(emails) == len(set(emails)), "Duplicate emails found"

        print(f"✅ User registered: {email}")

# Output: Demonstrating the contract in action
reg = RegisterUser()

# Perform registration
reg.register("user@example.com", "securepassword")
