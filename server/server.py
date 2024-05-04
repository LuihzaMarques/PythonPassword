import pymongo
# from utils import generate_password

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bancoSenha"]
collection = mydb["colecaoSenha"]
historyCollection = mydb["historicoSenha"]

def inserir_senha_banco(collection, password):
    mydict = {"senha": password}
    collection.insert_one(mydict)
    return

def remover_senha_banco(collection, query):
    collection.delete_one(query)
    return

def ver_senha_historico(collection):
    for i in collection.find({}, {"_id": 0}):
        print(i)
    return