from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Modelo para criação de item
class Item(BaseModel):
    name: str
    price: float

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

@app.get("/")
def hello_world():
    return {"Olá": "Mundo"}

@app.get("/teste")
def teste_api():
    lista = [1, 2, 3, 4, 5]
    return {"Números": [f"Número: {i}" for i in lista]}

# Base de dados para o CRUD
menu = [
    {   'id': 1,
        'name': 'coffee',
        'price': 2.5
     },
    {
        'id': 2,
        'name': 'cake',
        'price': 10
    },
    {
        'id': 3,
        'name': 'tea',
        'price': 3.2
    },
    {
        'id': 4,
        'name': 'croissant',
        'price': 5.79
    }
]

# Get 
@app.get('/get-item/{item_id}')
def get_item(
    item_id: int = Path(
    ...,  # O `...` é obrigatório e indica que o parâmetro é requerido
    description="Fill with ID of the item you want to view")):

    search = list(filter(lambda x: x["id"] == item_id, menu))

    if search == []:
        return {'Error': 'Item does not exist'}

    return {'Item': search[0]}

@app.get('/get-by-name')
def get_item(name: Optional[str] = None):

    search = list(filter(lambda x: x["name"] == name, menu))

    if search == []:
        return {'item': 'Does not exist'}

    return {'Item': search[0]}

@app.get('/list-menu')
def list_menu():
    return {'Menu': menu}

@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):

    search = list(filter(lambda x: x["id"] == item_id, menu))

    if search != []:
        return {'Error': 'Item exists'}

    item = item.dict()
    item['id'] = item_id

    menu.append(item)
    return item


@app.put('/update-item/{item_id}')
def update_item(item_id: int, item: UpdateItem):

    search = list(filter(lambda x: x["id"] == item_id, menu))

    if search == []:
        return {'Item': 'Does not exist'}

    if item.name is not None:
        search[0]['name'] = item.name

    if item.price is not None:
        search[0]['price'] = item.price

    return search


@app.delete('/delete-item/{item_id}')
def delete_item(item_id: int):
    search = list(filter(lambda x: x["id"] == item_id, menu))

    if search == []:
        return {'Item': 'Does not exist'}

    for i in range(len(menu)):
        if menu[i]['id'] == item_id:
            del menu[i]
            break
    return {'Message': 'Item deleted successfully'}