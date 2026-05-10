from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Name": "Kamrul Hasan Jaman"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/data")
def read_csv_data():
    df =pd.read_csv("Copy of AI adoption in Education.csv", encoding="utf-8")
    # Optional: Fill Nan values so the JSON is valid
    df = df.fillna("")
    return {"records": df.to_dict(orient="records")}

@app.get("/data/{index}")
def get_data_by_index(index: int):
    df = pd.read_csv("Copy of AI adoption in Education.csv", encoding="utf-8")
    data_list = df.to_dict(orient="records")

    # Check if the index exists in our list
    if index < 0 or index >= len(data_list):
        raise HTTPException(status_code=404, detail="Index out of range")

    return {
        "index": index,
        "row_data": data_list[index]
    }