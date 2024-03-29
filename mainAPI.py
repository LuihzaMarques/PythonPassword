import random  #importação da biblioteca random, usada para gerar números aleatórios
import string  #importação da biblioteca string, usada para a manipulação de strings

from fastapi import FastAPI  # importando fastAPI ; é uma classe python que fornece as funcionalidades para a API; 


""" comentários ...

* app é uma variavel que vira uma instancia de uma classe fastAPI. 

* o que é uma instância : é um objeto criado a partir de uma classe já existente. Portanto, ao criar esse objeto ele terá as mesma coisas (atritutos, métodos) da classe.

* exemplo: tem-se a classe FastAPI com todos os metodos e atributos para o desenvolvimento de uma API. Agora irei criar uma variavel X mas quero que ela tenha os mesmos
comportamentos da classe FastAPI, logo terei que instancia a classe FastAPI no atributo X .
            x = FastAPI()
    *** em termos gerais, uma instancia é um objeto criado a partir de uma classe. **** 

* o que está entre () são os argumentos passados para o construtor da classe. 

*   docs_url="/password" : URL usada para acessar a documentação/swagger -- http://localhost:8000/password
    redoc_url="/redocs":  URL do redocs -- http://localhost:8000/password
    title="Password API in Python" : titulo da API 
    description="API para geração de senhas" : descrição da API
    version="1.0" : versão da API
    openapi_url="/api/v1/opeanapi.json" : dados em json -- http://localhost:8000/password/opeanapi.json



"""

app = FastAPI(  
    docs_url="/password", #http://localhost:8000/password
    redoc_url="/redocs",   #http://localhost:8000/password
    title="Password API in Python",
    description="API para geração de senhas",
    version="1.0",
    openapi_url="/password/opeanapi.json", #http://localhost:8000/password/opeanapi.json
)

#declarações globais 
letras_maiusculas = string.ascii_uppercase #esta atribuido a variavel letras_maiusculas , uma constante do modulo String que contém letras de A - Z
letras_minusculas = string.ascii_lowercase #mesma coisa de cima 
numeros = string.digits #atribuindo a variavel numeros , uma constante do modulo string que contém os digitos 0-9
simbolos = '@#$%¨&*' #atribuindo a simblos os caracteres especificados em ' '

#estrutura da senha
caracteres = letras_maiusculas + letras_minusculas + numeros + simbolos

@app.post("/criar_nova_senha", tags=["new password"]) #define o endpoint Post para a rota /criar..   ; post pq estou criando um dado; 
async def criar_nova_senha():  #funcao assíncrona
    senha = ''.join(random.sample(caracteres, 15))
    '''logica da criação da senha; ''.joind (junta caracteres em uma única string) , random.sample() seleciona elementos
       neste caso 15, aleatoriamente da lista de caracteres, sem repetição. ''' 
    return {"nova_senha": senha}

@app.put("/tratar_senha_fraca", tags=["update password"]) #define o endpoint Put para a rota /trat... ; put atualiza os dados
async def tratar_senha_fraca(password: str): #funçao assíncrona com o parametro password; responsavel por validar a senha

    nova_senha = password   #atribuição
    #faltantes = {'maiusculas': '', 'minusculas': '', 'numeros': '', 'simbolos': ''}
    

    if not any(char.isupper() for char in password): #condicional
       ''' comentarios
            * for char in password : percorre o passwor
            * char.isupper() : verifica se o caracter é maiusculo; true or false
            * any() : verifica se há algo true dentro  ( )
            * if not : o not invente a condição
                    não executado:  se any(char.isupper() for char in password) | se for true o not passa pra not 
                    executado: se any(char.isupper() for char in password) | se for not o not passar pra true  
       '''
       # faltantes['maiusculas'] = random.choice(letras_maiusculas)
       nova_senha += random.choice(letras_maiusculas) #se a condição anterior for verdadeira essa linha é executada; add o caracter a password

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
    
    if len(nova_senha) < 15:  #if len verifica o cumprimento de uma string
        caracteres_faltantes = 15 - len(nova_senha) #calcula o que falta
        for _ in range(caracteres_faltantes):  # add 
            nova_senha += random.choice(string.ascii_letters + string.digits + '@#$%¨&*')
            return {"nova_senha": nova_senha}
    else :
       return {"a senha já é segura": password}


@app.get("/verifica_senha_segura", tags=["check password"]) #define o endpont get para a rota /verifi... ; get ler os daddos
async def verifica_senha_segura(password: str):  #assincrona com parametro password
   
    errors = [] #lista de erros 

   # mensagem = "A senha é segura."


    if not any(char in letras_maiusculas for char in password):
       errors.append("A senha não contém letra maiúscula.") # add a lista de erros
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
