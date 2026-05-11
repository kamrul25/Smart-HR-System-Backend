from fastapi import FastAPI
from pydantic import BaseModel

new = FastAPI()
# main_logic = FastAPI()

# Define Item model
class Item(BaseModel):
    name: str
    price: float

# Temporary in-memory storage
items ={}

# @main_logic.get("/")
@new.get('/')
def root():
    return{"name":"Fast APi","location":"From FastAPI"}

# Create
@new.post("/items/")
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, "item": item}

# Read
@new.get("/items/{item_id}")
async def read_item(item_id: int):
    return items.get(item_id,{"error":"Item not found"})


# Update
@new.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id in items:
        items[item_id] = item
        return {"message": "Item update", "item": item}
    return {"error": "Item not found"}

# Delete
@new.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in items:
        deleted_item = items.pop(item_id)
        return {"message": "Item Deleted", "item": deleted_item}
    return {"error":"Item not found"}


# To run the server use :
    # uvicorn app.new:new --reload 
    # uvicorn app.new:main_logic --reload 