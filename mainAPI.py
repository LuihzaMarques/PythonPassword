import random
import string
from fastapi import FastAPI
from datetime import datetime

from pydantic import BaseModel


class ResponseStatus(BaseModel):
    statusCode: int = 200
    data: dict = {}
    called_at: datetime = datetime.utcnow()
    path: str


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


@app.get("/criar_nova_senha")
async def criar_nova_senha():
    generated_password = generate_password()
    data = {"password": generated_password}
    return ResponseStatus(data=data, path="/criar_nova_senha")

    
@app.post("/tratar_senha_fraca")
async def tratar_senha_fraca(password: str):
    new_password = handle_weak_password(password)
    message = "Senha incrementada" if new_password != password else "Senha já é forte!"
    data = {"password": new_password}
    return ResponseStatus(data=data, message=message, path="/tratar_senha_fraca")


@app.get("/verifica_senha_segura")
async def verifica_senha_segura(password: str):
    result = check_secure_password(password)
    data = {"message": result}
    return ResponseStatus(data=data, path="/verifica_senha_segura")
