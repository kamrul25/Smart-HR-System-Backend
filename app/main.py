from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Smart HR System", version="1.0.0")

# --- Model ---
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

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

@app.put("/itemsPut/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}