from fastapi import FastAPI
from datetime import datetime
from utils.password_utils import generate_password, handle_weak_password, check_secure_password
from pydantic import BaseModel

class PassWord(BaseModel):
    senha: str
    descricao: str

passwords = []

class ResponseStatus(BaseModel):
    statusCode: int = 200
    data: dict = {}
    called_at: datetime = datetime.now()
    path: str


app = FastAPI(
    docs_url="/docs",
    title="Password API in Python",
    description="API para geração de senhas",
    version="1.0",
)

@app.post("/solicitar_senha")
async def solicitar_senha(desc:str):

    generated_password = generate_password()
    data = {generated_password: desc}
    passwords.append(PassWord(senha = generated_password,descricao = desc))
    message = "senha: " + generated_password + " finalidade: " + desc
    return ResponseStatus(data=data,message = message,path="/solicitar_senha")
    

@app.get("/listar_senhas")
async def listar_senhas():
   
    data = {}
    for senha in passwords:
        data[senha.senha] = senha.descricao
            
    return ResponseStatus(data=data,path="/listar_senhas")
   
    

         

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
