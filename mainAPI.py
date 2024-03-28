import random
import string

from fastapi import FastAPI

app = FastAPI(
    docs_url="/api/v1/password",
    redoc_url="/api/v1/redocs",
    title="Password API in Python",
    description="API para geração de senhas",
    version="1.0",
    openapi_url="/api/v1/opeanapi.json",
)

#declarações globais 
letras_maiusculas = string.ascii_uppercase
letras_minusculas = string.ascii_lowercase
numeros = string.digits
simbolos = '@#$%¨&*'

#estrutura da senha
caracteres = letras_maiusculas + letras_minusculas + numeros + simbolos

@app.post("/criar_nova_senha", tags=["new password"])
async def criar_nova_senha():
    senha = ''.join(random.sample(caracteres, 15))
    return {"nova_senha": senha}

@app.put("/tratar_senha_fraca", tags=["update password"])
async def tratar_senha_fraca(password: str):

    nova_senha = password
    #faltantes = {'maiusculas': '', 'minusculas': '', 'numeros': '', 'simbolos': ''}
    
    if not any(char.isupper() for char in password):
       # faltantes['maiusculas'] = random.choice(letras_maiusculas)
       nova_senha += random.choice(letras_maiusculas) 

    if not any(char.islower() for char in password):
       #faltantes['minusculas'] = random.choice(letras_minusculas)
      nova_senha += random.choice(letras_minusculas)

    if not any(char.isdigit() for char in password):
       # faltantes['numeros'] = random.choice(numeros)
       nova_senha += random.choice(numeros)

    if not any(char in '@#$%¨&*' for char in password):
       # faltantes['simbolos'] = random.choice(simbolos)
      nova_senha += random.choice(simbolos)

   # nova_senha = password + ''.join(faltantes.values())
    
    if len(nova_senha) < 15:
        caracteres_faltantes = 15 - len(nova_senha)
        for _ in range(caracteres_faltantes):
            nova_senha += random.choice(string.ascii_letters + string.digits + '@#$%¨&*')
            return {"nova_senha": nova_senha}
    else :
       return {"a senha já é segura": password}


@app.get("/verifica_senha_segura", tags=["check password"])
async def verifica_senha_segura(password: str):
   
    errors = []

   # mensagem = "A senha é segura."


    if not any(char in letras_maiusculas for char in password):
       errors.append("A senha não contém letra maiúscula.")
        #mensagem = "A senha não contém letra maiúscula."

 
    if not any(char in letras_minusculas for char in password):
        errors.append("A senha não contém letra minúscula.")
       # mensagem = "A senha não contém letra minúscula."


    if not any(char in numeros for char in password):
        errors.append("A senha não contém número.")
       # mensagem = "A senha não contém número."


    if not any(char in simbolos for char in password):
      errors.append("A senha não contém símbolo.")
      # mensagem = "A senha não contém símbolo."


    if errors:
       return {"errors": errors}
    else:
        return {"mensagem": "A senha é segura."}
   

    #return {"mensagem": mensagem}
