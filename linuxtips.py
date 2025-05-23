from fastapi import FastAPI
from enum import Enum

app = FastAPI() # Não é mais um app WSGI e sim ASGI (consegue lidar com Views assíncronas)

class ListOption(str, Enum):
    user = "user"
    department = "department"
    account = "account"    

# Agora usamos o async - logo, ele já consegue trabalhar com serializador de json (não precisamos importar nada mais)
'''
@app.get("/") # Setando primeira rota
async def hello(): # Se é async é co-rotina
    return {"message": "Hello World!"}
'''

@app.get("/{list_option}/list")
async def generic_list(list_option: ListOption): 
    if list_option == ListOption.user: 
        data = ["jim", "pam", "dwight"]
    elif list_option == ListOption.department:
        data = ["Sales", "Management", "IT"]
    elif list_option == ListOption.account:
        data = [1212, 4354, 4546, 6777]

    return {list_option: data}

@app.get("/user/{username}") # Path/Roteamento
async def user_profile(username: str):
    return {"data": username}

@app.get("/account/{number}")
async def account_detail(number: int):
    return {"number": number}


# Trabalhando com arquivos
@app.get("import/{filepath:path}")
async def import_file(filepath: str):
    return {"importing": filepath}
