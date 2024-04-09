import random
import string

def generate_password(length: int = 15) -> str:
    symbols = string.punctuation
    charset = string.ascii_letters + string.digits + symbols
    return "".join(random.sample(charset, length))


def handle_weak_password(password: str) -> str:
    new_password = password

    symbols = string.punctuation
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits

    charset = symbols + uppercase + lowercase + digits

    # Check password length
    if len(password) < 15:
        missing_chars = 15 - len(password)
        new_password += "".join(random.choices(charset, k=missing_chars))

    # Check missing characters (using list comprehension)
    if not any(char.isupper() for char in password):
        new_password += random.choice(uppercase)
    if not any(char.islower() for char in password):
        new_password += random.choice(lowercase)
    if not any(char.isdigit() for char in password):
        new_password += random.choice(digits)
    if not any(char in symbols for char in password):
        new_password += random.choice(symbols)

    return new_password


def check_secure_password(password: str) -> str:
    errors = []

    if not any(char.isupper() for char in password):
        errors.append("A senha não contém letra maiúscula.")
    if not any(char.islower() for char in password):
        errors.append("A senha não contém letra minúscula.")
    if not any(char.isdigit() for char in password):
        errors.append("A senha não contém número.")
    if not any(char in string.punctuation for char in password):
        errors.append("A senha não contém símbolo.")

    if errors:
        return ", ".join(errors)  # Return comma-separated errors
    else:
        return "Senha forte!"