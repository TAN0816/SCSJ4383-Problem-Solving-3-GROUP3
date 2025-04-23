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

    def check_invariants(self):
        emails = [u["email"] for u in self.users]
        assert len(emails) == len(set(emails)), "Invariant violated: Duplicate emails found"

    def register(self, email, password):
        # --- Pre-condition checks ---
        assert email and "@" in email, "Precondition failed: Email must be in a valid format"
        assert len(password) >= 8, "Precondition failed: Password must be at least 8 characters"
        assert self.is_email_unique(email), "Precondition failed: Email is already registered"

        # --- Process ---
        hashed_pw = self.hash_password(password)
        self.users.append({"email": email, "password": hashed_pw})

        # --- Post-condition check ---
        assert any(u["email"] == email for u in self.users), "Postcondition failed: User was not added"

        # --- Invariant check ---
        self.check_invariants()

        print(f"User registered: {email}")

# Output: Demonstrating the contract in action
reg = RegisterUser()

# Perform registration
reg.register("user@example.com", "securepassword")

# Uncomment to test violations:
# reg.register("user@example.com", "anotherpass")   # Fails: email already exists
# reg.register("invalidemail", "12345678")          # Fails: invalid email format
# reg.register("new@example.com", "short")          # Fails: password too short