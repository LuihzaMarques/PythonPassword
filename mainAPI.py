import string
import random
from fastapi import FastAPI

app = FastAPI()

letras_maiusculas = string.ascii_uppercase
letras_minusculas = string.ascii_lowercase
numeros = string.digits
simbolos = '@#$%¨&*'

caracteres = letras_maiusculas + letras_minusculas + numeros + simbolos

@app.post("/criar_nova_senha")
async def criar_nova_senha():
    senha = ''.join(random.sample(caracteres, 15))
    return {"nova_senha": senha}

@app.put("/tratar_senha_fraca")
async def tratar_senha_fraca(password: str):
    faltantes = {'maiusculas': '', 'minusculas': '', 'numeros': '', 'simbolos': ''}
    
    if not any(char.isupper() for char in password):
        faltantes['maiusculas'] = random.choice(letras_maiusculas)

    if not any(char.islower() for char in password):
        faltantes['minusculas'] = random.choice(letras_minusculas)

    if not any(char.isdigit() for char in password):
        faltantes['numeros'] = random.choice(numeros)

    if not any(char in '@#$%¨&*' for char in password):
        faltantes['simbolos'] = random.choice(simbolos)

    nova_senha = password + ''.join(faltantes.values())
    
    if len(nova_senha) < 15:
        caracteres_faltantes = 15 - len(nova_senha)
        for _ in range(caracteres_faltantes):
            nova_senha += random.choice(string.ascii_letters + string.digits + '@#$%¨&*')
            
    return {"nova_senha": nova_senha}

@app.get("/verifica_senha_segura")
async def verifica_senha_segura(password: str):
    errors = []

    if not any(char in letras_maiusculas for char in password):
        errors.append("A senha não contém letra maiúscula.")

    if not any(char in letras_minusculas for char in password):
        errors.append("A senha não contém letra minúscula.")

    if not any(char in numeros for char in password):
        errors.append("A senha não contém número.")

    if not any(char in simbolos for char in password):
        errors.append("A senha não contém símbolo.")
    
    if errors:
        return {"errors": errors}
    else:
        return {"mensagem": "A senha é segura."}
