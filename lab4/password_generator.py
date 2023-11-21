"""
This module provides functionality to generate a password, optionally salt it,
hash it using a selected algorithm, and write the password details to a CSV file.
Supported hashing algorithms include MD5, SHA256, SHA512, bcrypt, scrypt, and argon2id.
"""

import secrets
import string
import hashlib
import csv  # Import the CSV module
from passlib.hash import bcrypt, scrypt, argon2


def generate_password(length=8):
    """
    Generates a random password using a combination of ASCII letters,
    digits, and punctuation characters.

    :param length: Length of the password to be generated, defaults to 8 if not provided.
    :return: A string representing the generated password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(characters) for i in range(length))


def add_salt(password):
    """
    Salts the provided password with a random sequence of ASCII letters and digits.

    :param password: The original password to be salted.
    :return: A new string representing the salted password.
    """
    salt = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(26)
    )
    return salt + password


def hash_password(password, algorithm):
    """
    Hashes a password using the specified cryptographic hash function.

    :param password: The password to be hashed.
    :param algorithm: A string indicating the hash function to use
    (md5, sha256, sha512, bcrypt, scrypt, argon2id).
    
    :return: A string representing the hashed password.
    :raises ValueError: If an invalid hashing algorithm is provided.
    :raises TypeError: If the input data is of the wrong type.
    :raises Exception: For specific hashing library exceptions.
    """

    options = {
        "md5": lambda pwd: hashlib.md5(pwd.encode(), usedforsecurity=False).hexdigest(),
        "sha256": lambda pwd: hashlib.sha256(pwd.encode(), usedforsecurity=False).hexdigest(),
        "sha512": lambda pwd: hashlib.sha512(pwd.encode(), usedforsecurity=False).hexdigest(),
        "bcrypt": lambda pwd: bcrypt.hash(pwd),
        "scrypt": lambda pwd: scrypt.hash(pwd),
        "argon2id": lambda pwd: argon2.using(type="ID").hash(pwd)
    }

    try:
        hash_function = options.get(algorithm)
        if hash_function is None:
            raise ValueError("Invalid hashing algorithm")
        return hash_function(password)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Hashing error due to input: {str(e)}")
    except (bcrypt.exceptions.BcryptError, 
            scrypt.error, 
            argon2.exceptions.Argon2Error) as e:
        raise Exception(f"Error in hashing library: {str(e)}")


def main():
    """
    Main execution function that prompts the user for password preferences,
    generates or takes a user-defined password, salts if desired, hashes it
    with a chosen algorithm, and writes the details to a CSV file.
    """
    print("Welcome to the Password Generator and Hasher")

    choice = input("Do you want to input your own password? (yes/no): ").lower()

    if choice == "yes":
        password = input("Enter your password: ")
    else:
        length = int(input("Enter the desired length of your password: "))
        password = generate_password(length)

    add_salt_choice = input(
        "Do you want to add salt to your password? (yes/no): "
    ).lower()
    is_salted = False  # Initialize the salt status

    if add_salt_choice == "yes":
        password = add_salt(password)
        is_salted = True  # Set salt status to True if salt is added
        print(f"Generated Password with Salt: {password}")
    else:
        print(f"Generated Password: {password}")

    print("Choose a hashing algorithm: md5, sha256, sha512, bcrypt, scrypt, argon2id")
    algorithm = input("Enter your choice: ").lower()

    hashed_password = hash_password(password, algorithm)
    print(f"Hashed Password ({algorithm}): {hashed_password}")

    # Open a CSV file in write mode
    with open("passwords.csv", "a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the password, hashed password, salt status, and algorithm to the CSV file
        writer.writerow(
            [
                password,
                hashed_password,
                algorithm,
                "Salted" if is_salted else "Not Salted",
            ]
        )


if __name__ == "__main__":
    main()
