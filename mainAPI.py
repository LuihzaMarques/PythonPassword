import random
import string

from fastapi import FastAPI


app = FastAPI(
    docs_url="/docs",
    title="Password API in Python",
    description="API para geração de senhas",
    version="1.0",
)


def generate_password(length: int = 15) -> str:
    symbols = string.punctuation
    charset = string.ascii_letters + string.digits + symbols
    return "".join(random.sample(charset, length))


def handle_weak_password(password: str) -> dict:
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

    return {
        "weak": password != new_password,
        "password": new_password,
    }


def check_secure_password(password: str) -> dict:
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
        return {"weak": True, "errors": errors}
    else:
        return {"weak": False, "message": "password strong."}


@app.get("/criar_nova_senha")
async def criar_nova_senha():
    generated_password = generate_password()
    return {"password": generated_password}


@app.post("/tratar_senha_fraca")
async def tratar_senha_fraca(password: str):
    result = handle_weak_password(password)
    new_password = result["password"]

    if result["weak"]:
        return {"password": new_password, "message": "Senha incrementada"}
    else:
        return {"password": new_password, "message": "Senha já é forte!"}


@app.get("/verifica_senha_segura")
async def verifica_senha_segura(password: str):
    result = check_secure_password(password)
    return result
