import bcrypt


class PasswordManager:
    """
    A class for securely encrypting and verifying passwords using bcrypt.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt.

        :param password: The plain text password to be hashed.
        :return: The hashed password as a string.
        """
        salt = bcrypt.gensalt()  # Generate a salt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")  # Convert bytes to string for storage

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password.

        :param password: The plain text password to verify.
        :param hashed_password: The stored hashed password.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
