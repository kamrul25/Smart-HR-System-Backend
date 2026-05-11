from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Smart HR System", version="1.0.0")

# --- Model ---
class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Optional[bool] = None

items: List[Item] = []
# --- Data Loading (Load once on startup) ---
# This saves time and memory for every request
try:
    df_global = pd.read_csv("Copy of AI adoption in Education.csv", encoding="utf-8")
    df_global = df_global.fillna("")
  
except FileNotFoundError:
    print("Warning: CSV file not found. Data routes will fail.")
    df_global = pd.DataFrame()

# --- Routes ---

@app.get("/")
def read_root():
    return {"System": "Smart HR", "Admin": "Kamrul Hasan Jaman"}


@app.get("/data")
def read_csv_data():
    # orient="records" is perfect for frontend tables
    return {"records": df_global.to_dict(orient="records")}

@app.get("/data/{index}")
def get_data_by_index(index: int):
    # Check bounds using the global dataframe
    if index < 0 or index >= len(df_global):
        raise HTTPException(status_code=404, detail=f"Index {index} out of range")

    return {
        "index": index,
        "row_data": df_global.iloc[index].to_dict()
    }


@app.get("/items")
def all_items():
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items")
def add_item(item: Item):
    # FIXED: append the instance 'item', not the class 'Item'
    items.append(item) 
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, update_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = update_item
            return {"item_id": item_id, "updated_item": update_item}
    
    # FIXED: Use 'raise' instead of 'return'
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def deleted_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            # FIXED: pop using the 'index' from the loop
            deleted = items.pop(index)
            return deleted
    
    # FIXED: Use 'raise' instead of 'return'
    raise HTTPException(status_code=404, detail="Item not found")


# Crete a partial model where every field is optional
class ItemPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[str] = None
    is_offer: Optional[bool] = None

patch_items: List[ItemPatch] = []
def patch_item(item_id: int, item_update: ItemPatch):
    for index, existing_item in enumerate(patch_items):
        if existing_item.id == item_id:
            update_data = item_update.model_dump(exclude_unset=True)
            update_item_patch= existing_item.model_copy(update=update_data)

            # Save back to the list
            patch_items[index] = update_item_patch
            return {"item_id": item_id, "updated_item":update_item_patch}
    
    raise HTTPException(status_code=404, detail="Item not found")
