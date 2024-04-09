import utils.password_utils as utils
from fastapi import FastAPI

app = FastAPI(
    docs_url="/docs",
    title="Password API in Python",
    description="API para geração de senhas",
    version="1.0",
)


def generate_password(length: int = 15) -> str:
    symbols = utils.string.punctuation
    charset = utils.string.ascii_letters + utils.string.digits + symbols
    return "".join(utils.random.sample(charset, length))


def handle_weak_password(password: str) -> dict:
    new_password = password

    symbols = utils.string.punctuation
    uppercase = utils.string.ascii_uppercase
    lowercase = utils.ascii_lowercase
    digits = utils.string.digits

    charset = symbols + uppercase + lowercase + digits

    # Check password length
    if len(password) < 15:
        missing_chars = 15 - len(password)
        new_password += "".join(utils.random.choices(charset, k=missing_chars))

    # Check missing characters (using list comprehension)
    if not any(char.isupper() for char in password):
        new_password += utils.random.choice(uppercase)
    if not any(char.islower() for char in password):
        new_password += utils.random.choice(lowercase)
    if not any(char.isdigit() for char in password):
        new_password += utils.random.choice(digits)
    if not any(char in symbols for char in password):
        new_password += utils.random.choice(symbols)

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
    if not any(char in utils.string.punctuation for char in password):
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
